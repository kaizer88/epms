from django import forms

from .models import EPMUser, Employee


class LoginForm(forms.ModelForm):
    employee_code = forms.CharField(label='Employee Number', widget=forms.TextInput(
        attrs={'placeholder': 'Employee Number'}),
                                      )
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}),
                               )

    class Meta:
        model = EPMUser
        exclude = ('last_login', 'is_active', 'date_joined', 'is_staff', 'is_superuser',
                   'groups', 'user_permissions', 'first_name', 'last_name', 'email',)
        fields = ['employee_code', 'password']


class PasswordRestForm(forms.Form):

    email = forms.EmailField(label='Email Address')

    # class Meta:
    #     model = EPMUser
    #     exclude = ('last_login', 'is_active', 'date_joined', 'is_staff', 'is_superuser',
    #                'groups', 'user_permissions', 'first_name', 'last_name','employee_code', 'password')
    #     fields = ['email']


class PasswordUpdateForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:

        fields = ['password', 'password2']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2


class ProfileForm(forms.ModelForm):

    # salary_level = forms.ChoiceField(forms.Select)

    class Meta:
        model = Employee
        exclude = ['is_first_login', 'user']
        fields = ['date_of_birth', 'gender', 'title', 'first_name', 'last_name', 'job_title',
                  'department', 'emp_status', 'disability_status', 'salary_level', 'salary_notch',
                  'is_supervisor']
