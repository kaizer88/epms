import uuid
import logging
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Project, ProjectType, Status
# from .models import Organisation, Programme, Branch, Component, Project, ProjectType, Status
from accounts.models import Employee
from organisation.models import Programme, SubProgramme

from permissions.views import add_project_manager_as_contr, add_access_details, update_project_access_details
from permissions.models import Signature, ActiveProjectAccessDetails, Contributor, AccessLevel

logger = logging.getLogger(__name__)


@login_required()
def add_project(request):

    # TODO design on proper numbering pattern for project no
    project_no = uuid.uuid4()
    programme = Programme.objects.get(id=request.POST['programme'])
    p_type = ProjectType.objects.get(id=request.POST['p_type'])
    p_status = Status.objects.get(name='undefined')

    start = request.POST.get('p_start', None)
    end = request.POST.get('p_end', None)
    start_date = end_date = ""
    if start:
        start_date = datetime.strptime(start, "%d/%m/%Y")
        start_date = datetime.strftime(start_date, '%Y-%m-%d')
    if start:
        end = datetime.strptime(end, "%d/%m/%Y")
        end_date = datetime.strftime(end, '%Y-%m-%d')

    try:   # add new project
        project = Project.objects.create(
            organisation=request.user.employee.organisation,
            branch=request.user.employee.branch,
            component=request.user.employee.component,
            project_manager=request.user.employee,
            programme=programme,
            name=request.POST['name'],
            start_date=start_date,
            end_date=end_date,
            project_type=p_type,
            budget=request.POST['budget'],
            report_cycle=request.POST['r_cycle'],
            templates=request.POST['temps'],
            plan=request.POST['plan'],
            risk=request.POST['risk'],
            number=project_no,
            details=request.POST['details'],
            comments=request.POST['comments'],
            sponsor=request.POST['sponsor'],
            status=p_status
        )
        # add current user as project contributor to this particular project
        contributor, employee = add_project_manager_as_contr(
            request, project_no=project_no, employee_code=request.user.employee_code, sign_pos=1,
            note='project administrator', projec=project)
        if request.POST['sign'] == 'true':
            sign(request, project=project, employee=employee, token=1)
            update_project_access_details(request, project=project, contributor=contributor)
            is_next = has_next_contr(request, project=project)
            if is_next:
                update_project_access_details(request, project=project, contributor=is_next)
        else:
            sign(request, project=project, employee=employee, token=4)
        return JsonResponse({
            'status': 200,
            'message': "Successfully Saved New Project: {}".format(request.POST['name'])
        })
    except ValidationError as e:
        logger.warning(e)
        return JsonResponse({
            'status': 40,
            'message': 'Input Error'
        })


def has_next_contr(request, **kwargs):

    current_emp = Contributor.objects.filter(employee=request.user.employee, project=kwargs.get("project")).values(
        "queue_position").get()
    next_emp_place = (current_emp["queue_position"]) + 1
    try:
        contributor = Contributor.objects.get(queue_position=next_emp_place, project=kwargs.get('project'))
        return contributor
    except ObjectDoesNotExist as e:
        logger.exception("contr not found: %s" % e)


def get_pm_as_contr(request, **kwargs):
    try:
        contributor = Contributor.objects.get(employee=kwargs.get("project").project_manager)
        return contributor
    except ObjectDoesNotExist as e:
        logger.exception("contr not found: %s" % e)


@login_required()
def sign(request, **kwargs):
    contr = Contributor.objects.get(employee=kwargs.get("employee"), project=kwargs.get("project"))
    Signature.objects.update_or_create(
        contributor=contr, project=kwargs.get("project"),
        defaults={'token': kwargs.get("token", 3)},
    )


@login_required()
def read_projects(request):

    emp_projects = Project.objects.filter(project_manager=request.user.employee).values(
                                                                'id', 'name', 'start_date',
                                                                'end_date', 'programme__name',
                                                                'created', 'status__name').order_by('-created')
    projects = [proj for proj in emp_projects]
    return JsonResponse({
        "results": "OK",
        "message": "Loading projects",
        "emp_projects": projects,
    })


@login_required()
def get_employee_info(request):
    employee = Employee.objects.filter(user=request.user).values('component__name',
                                                                 'branch__name',
                                                                 'organisation__name',
                                                                 'branch__programme',
                                                                 )
    prog_ids = []
    for i in employee:
        if i['branch__programme']:
            prog_ids.append(i['branch__programme'])

    programmes = []
    for i in prog_ids:
        programme = Programme.objects.filter(id=i).values('name', 'id')
        programmes.append([x for x in programme])
    p_types = ProjectType.objects.all().values()
    _type = [field for field in p_types]
    emp = [field for field in employee]
    return JsonResponse({'emp': emp[0],
                         'progs': programmes,
                         'types_': _type,
                         })


@login_required()
def read_project(request):

    project_req = Project.objects.select_related()
    project = project_req.filter(id=request.GET['proj']).values(
        'component__name', 'branch__name', 'organisation__name', 'component__name', 'number',
        'project_manager__first_name', 'project_manager__last_name', 'status__name',
        'status__id',  'templates', 'plan', 'budget',  'details', 'risk', 'comments', 'start_date',  'end_date',
        'programme__name', 'sponsor',  'name',  'project_type__name', 'id',
                                                                )
    proj = [field for field in project]
    project_statuses = Status.objects.all().values()
    status = [s for s in project_statuses]
    """
    check if the token is not 3, ie unsigned
    check if the current user has someone above it
    make it readonly if someone is above
    """
    is_signed = Signature.objects.get(project=request.GET['proj'])
    if is_signed.token != 3:  # project is unsigned
        proj_obj = Project.objects.get(id=request.GET['proj'])  # try to optimize this call, its a resource waste
        is_next = has_next_contr(request, project=proj_obj)  # check if there is a signatory above current user
        if is_next:  # if there is one, make the form readonly
            write = False
        else:
            write = True
    else:
        write = True
    return JsonResponse({'project': proj,
                         'status': status,
                         'write': write
                         })


@login_required()
def update_project(request):

    try:
        obj = Project.objects.get(id=request.POST['id'])
        contr = Contributor.objects.filter(employee=request.user.employee, project=obj)
        for key, value in request.POST.items():
            if (key, value) == ('sig', 'true'):
                if has_write_access(contr):
                    sign(request, project=obj, employee=obj.project_manager, token=1)
                    update_project_access_details(request, project=obj, contributor=contr)
                else:
                    logger.info("User: has not write permission and attempts to sign project:".format(contr, obj))
                    return JsonResponse({"results": "Error", "message": "Error. You do not have permission to sign"})
            if key != 'status':
                setattr(obj, key, value)
            if key == 'status':
                setattr(obj, key, Status.objects.get(id=value))
        obj.save()
        has_next = has_next_contr(request, project=obj)
        if has_next:
            try:
                update_project_access_details(request, project=obj, contributor=has_next)
            except ObjectDoesNotExist:
                pass
        return JsonResponse({"status": 200, "message": "Project updated successfully"})
    except Project.DoesNotExist:
        logger.warning("Project with id: '{}' does not existing.".format(request.POST['id']))
        return JsonResponse({'status': 52, "message": "Failed to update"})


@login_required()
def get_active_project(request):
    active_project = Project.objects.filter(project_manager=request.user.employee, is_active=True).values(
        'number', 'name')
    projects = [proj for proj in active_project]
    return JsonResponse({
        'projects': projects
    })


@login_required()
def get_contr_project(request):

    contr = Contributor.objects.get(employee=request.user.employee)
    user_project = Project.objects.select_related().filter(number=contr.project.number).values(
        'component__name', 'branch__name', 'organisation__name', 'component__name', 'number',
        'project_manager__first_name', 'project_manager__last_name', 'status__name',
        'status__id',  'templates', 'plan', 'budget',  'details', 'risk', 'comments', 'start_date', 'end_date',
        'programme__name', 'sponsor',  'name',  'project_type__name'
                                                                )
    access = which_access(contr)
    project = [field for field in user_project]
    return JsonResponse({'project': project,
                         'access': access
                         })


@login_required()
def contributor_signs(request):
    contr = Contributor.objects.get(employee=request.user.employee)
    project = Project.objects.get(number=request.POST["project"])
    if has_write_access(contr):  # if user has read access, exit
        Signature.objects.update_or_create(
            contributor=contr, project=project,
            defaults={'token': request.POST.get("token")}
        )
        logger.info("user: {} successfully signs project: {}".format(contr, project))
        update_project_access_details(request, project=project, contributor=contr)
        if request.POST['token'] == '2':
            is_pm = get_pm_as_contr(request, project=project)
            update_project_access_details(request, project=project, contributor=is_pm)
            return JsonResponse({"results": "OK", "message": "Signed Successfully"})
        else:
            is_next = has_next_contr(request, project=project)
            if is_next:
                update_project_access_details(request, project=project, contributor=is_next)
                return JsonResponse({"results": "OK", "message": "Signed Successfully"})
            else:
                pass
    else:
        logger.info("User without permission to sign attempts to sign")
        return JsonResponse({"results": "Error", "message": "Error. You do not have permission to sign"})


def has_write_access(contr):
    access = ActiveProjectAccessDetails.objects.get(contributor=contr)
    if access.access_level.mode == "2":  # if user has read access, exit
        return True
    else:
        return False


def which_access(contr, proj_obj):
    accessibility = ActiveProjectAccessDetails.objects.filter(contributor=contr, project=proj_obj).values('access_level__mode')
    if accessibility:
        print(accessibility)
        return [i["access_level__mode"] for i in accessibility]
    else:
        return "read"  # read access


@login_required()
def get_contributors(request):

    employee = Employee.objects.get(user=request.user)
    people = Contributor.objects.filter(project__project_manager=employee).values(
                    "note", "employee__first_name", "employee__last_name",
                    "queue_position", "employee__user__employee_code",
                    "project__name", "project__status"
                 )
    contributors = [p for p in people]
    return JsonResponse({
        "results": "OK",
        "message": "Loading project contributors",
        "people": contributors
    })


@login_required()
def read_subprogramme(request):

    programme = Programme.objects.get(id=request.GET['programme'])
    sub_programme = SubProgramme.objects.filter(programme=programme).values('name', 'id')
    sub_progs = [field for field in sub_programme]
    return JsonResponse({'sub_progs': sub_progs})
