from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models import Employee


@login_required()
def dashboard(request):
    template = 'home/dashboard.html'
    profile = Employee.objects.get(user=request.user)
    return render(request, template, context={'profile': profile})
