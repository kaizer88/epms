import uuid
import logging

from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from accounts.models import Employee
from .models import AccessLevel, Contributor, ActiveProjectAccessDetails
from programme_project.models import Project


logger = logging.getLogger(__name__)


def add_project_manager_as_contr(request, **kwargs):
    """ add new contributor to the project"""

    employee = Employee.objects.get(user__employee_code=kwargs.get('employee_code'))
    project = Project.objects.filter(project_manager=request.user.employee, is_active=True).order_by('-created')[0]
    access_level = AccessLevel.objects.get(mode='read')
    contr = Contributor.objects.create(
        employee=employee,
        queue_position=kwargs.get('sign_pos'),
        project=project,
        note=kwargs.get('notes', None),
    )
    add_access_details(request, project=project, access_level=access_level, contributor=contr)
    return contr, employee


@login_required()
def add_contributor(request):
    """ add new contributor to the project"""

    try:
        employee = Employee.objects.get(user__employee_code=request.POST['employee_code'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "status": 41,
            "message": "Error. Could not find employee with Persal: {}".format(request.POST['employee_code'])
        })
    project = Project.objects.get(number=request.POST['project'])
    access_level = AccessLevel.objects.get(mode='read')
    try:
        contr = Contributor.objects.create(
            employee=employee,
            queue_position=request.POST['sign_pos'],
            project=project,
            note=request.POST.get('notes', None),
        )
    except IntegrityError:
        return JsonResponse({
            "status": 52,
            "message": 'Employee: {} is already added to project: {}'.format(request.POST['employee_code'], project.name)
        })
    else:
        add_access_details(request, project=project, access_level=access_level, contributor=contr)
    return JsonResponse({"status": 200,
                         "message": "Successfully added Employee: {} into Project: {}".format(
                            request.POST['employee_code'],
                            project.name
                          )
                         })


def add_access_details(request, **kwargs):

    p = ActiveProjectAccessDetails.objects.create(
        uuid=uuid.uuid4(),
        access_level=kwargs.get("access_level"),
        contributor=kwargs.get("contributor"),
        project=kwargs.get("project")
    )
    return p.uuid


@login_required()
def update_project_access_details(request, **kwargs):
    project_access = ActiveProjectAccessDetails.objects.select_related().get(
        contributor=kwargs.get("contributor"), project__number=kwargs.get("project").number
                                                                          )
    active_access = AccessLevel.objects.get(name=project_access.access_level)
    new_access = AccessLevel.objects.exclude(name=active_access).get()
    project_access.access_level = new_access
    project_access.save()
