from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import Supervisor, Employee


def get_supervisors(request):

    employee = Employee.objects.get(user=request.user)
    query_results = Supervisor.objects.select_related().filter(Q(employees=employee)).values(
        'name__user__employee_code', 'name__first_name', 'name__last_name')
    results = [x for x in query_results]
    return JsonResponse({
        'results': results
    })
