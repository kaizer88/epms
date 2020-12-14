# core django imports
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# app level imports
from .forms import LoginForm, PasswordRestForm, PasswordUpdateForm, ProfileForm
from .models import EPMUser, Token, Employee


def auth(request):
    template = 'accounts/auth.html'
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        employee_code = form.data['employee_code']
        password = form.data['password']
        user = authenticate(employee_code=employee_code, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/dashboard/')
        form = LoginForm()
    return render(request, template, {'login_form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def pass_reset(request):

    template = 'accounts/password_reset.html'
    form = PasswordRestForm()
    if request.method == 'POST':
        form = PasswordRestForm(request.POST)
        emp_email = form.data['email']
        if form.is_valid():
            try:
                validate_email(emp_email)
                send_reset_link(emp_email)
                return redirect('/password_reset/done/')
            except Exception as e:
                print("address not found", e)
                raise e
    return render(request, template, {'pass_reset': form})


def validate_email(email):

    employee = get_object_or_404(EPMUser, email=email)

    return employee


def send_reset_link(email):
    """
    create the dest url with a hash for the key
    set the links expire date

    :param email:
    :return:
    """
    send_mail(
        'Password reset',
        'Here is a link to reset your password',
        'admin@avortech.co.za',
        [email],
    )


def password_reset_done(request):

    return render(request, template_name='accounts/password_reset_done.html')


def password_update(request, user=None, token=None):

    template = 'accounts/password_reset_confirm.html'
    form = PasswordUpdateForm()
    if request.method == 'POST':
        form = PasswordUpdateForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            user = EPMUser.objects.get(employee_code=user, token__token=token,
                                       token__token_is_used=False)
            Token.objects.filter(token=token).update(
                token_is_used=True
            )
            user.set_password(password)
            user.save()
            return redirect('password_complete')
    return render(request, template, {'pass_update': form})


def password_reset_complete(request):

    return render(request, template_name='accounts/password_reset_complete.html')


@login_required()
def display_profile(request):
    template = 'accounts/profile.html'

    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST or None, instance=user)
        if form.is_valid():
            if form.has_changed():
                if 'supervisor' in form.changed_data:
                    notify_supervisor(request.POST['supervisor'])
            form.save()
            return redirect('/dashboard/')
    else:
        form = ProfileForm(instance=user)
    return render(request, template, {'profile': form})


def notify_supervisor(supervisor):
    """
    Sends notification to supervisor
    :param supervisor:
    :return:
    """
    super_v = Employee.objects.get(pk=supervisor)
    send_mail(
        'Confirmation',
        'Please confirm if you are a supervisor to',
        'admin@avortech.co.za',
        [super_v.user.email],
    )
