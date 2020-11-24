import uuid
import logging
import json
import uuid
from datetime import datetime, date

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import Framework, Risk, KeyPerformanceIndicator, AnnualTarget, Goal, Objective, Imperatives, \
    StrategicOutput, ResourcePlan, Subprogramme
from accounts.models import Employee
from organisation.models import Branch, Programme, SubProgramme

from .forms import StrategyForm, OverviewForm
from .models import Overview

logger = logging.getLogger(__name__)


@login_required()
def get_employee_info(request):
    employee = Employee.objects.filter(user=request.user).values('component__name',
                                                                 'branch__name',
                                                                 'organisation__name',
                                                                 )
    emp = [e for e in employee]
    return JsonResponse({
        'emp': emp
    })


def get_employee_branch(request):
    employee = Employee.objects.get(user=request.user)
    return employee.branch


def get_or_create_overview(request):

    branch = get_employee_branch(request)
    if Overview.objects.filter(branch=branch, is_signed=False):
        overview = Overview.objects.filter(branch=branch).values().latest('created')
        return JsonResponse({
            'overview': overview,
            'is_signed': False
        })

    elif Overview.objects.filter(branch=branch, is_signed=True):
        overview = Overview.objects.select_related().filter(branch=branch).values().latest('created')
        return JsonResponse({
            'overview': overview,
            'is_signed': True
        })


@login_required()
def save_new_overview(request):
    if request.method == 'POST' and request.is_ajax():
        obj, created = Overview.objects.update_or_create(
            branch=Branch.objects.get(name=request.POST['branch']),
            defaults={
                'priority_programme': request.POST.get('priority', None),
                'vision': request.POST.get('vision', None),
                'analysis': request.POST.get('vision', None),
                'risks': request.POST.get('risks', None),
                'values': request.POST.get('values', None),
                'goals': request.POST.get('goals', None),
                'revisions': request.POST.get('revisions', None),
                'mtef_budget': request.POST.get('budget', 0.0) if request.POST['budget'] is not "" else 0.0,
                'mission': request.POST.get('mission', None)
            },
        )
        if created:
            return JsonResponse({'status': 200, 'message': "New Strategic Overview created successfully"})
        else:
            return JsonResponse({'status': 200, 'message': "Strategic Overview updated successfully"})


@login_required()
def update_overview(request):
    if request.method == 'POST' and request.is_ajax():
        # TODO add error handling here
        Overview.objects.filter(id=39).update(
            priority_programme=request.POST.get('priority', None),
            vision=request.POST.get('vision', None),
            analysis=request.POST.get('analysis', None),
            risks=request.POST.get('risks', None),
            values=request.POST.get('values', None),
            goals=request.POST.get('goals', None),
            revisions=request.POST.get('revisions', None),
            mtef_budget=request.POST.get('mtef_budget', None)
        )


@login_required()
def sign(request):
    if request.method == 'POST' and request.is_ajax():
        employee = Employee.objects.get(user=request.user)
        obj, created = Overview.objects.update_or_create(
            branch=Branch.objects.get(name=employee.branch),
            defaults={
                'is_signed': True,
                'signed_user': employee
            },
        )
        if not created:
            return JsonResponse({'status': 200, 'message': "Strategic Overview signed-off successfully"})


@login_required()
def create_objective_goal(request):

    if request.POST['goal']: # TODO implement a front-end validation instead
        Goal.objects.create(
            framework=Framework.objects.latest('created'),
            goal_id=uuid.uuid4(),
            goal=request.POST.get('goal', None),
            statement=request.POST.get('statement', None)
        )
        return JsonResponse({'status': 200, 'message': "Goal saved successfully"})
    else:
        return JsonResponse({'status': 52, 'message': "Error, Goal field cannot be left blank"})


def read_employee_info(request):
    employee = Employee.objects.filter(user=request.user).values('component__name',
                                                                 'branch',
                                                                 'organisation__name',
                                                                 'branch__programme',
                                                                 'branch__programme__subprogramme',
                                                                 'programme',
                                                                 )
    emp = [e for e in employee]
    return {"employee": emp}


@login_required()
def create_objective(request):

    employee = read_employee_info(request)
    branch = employee["employee"][0]['branch']
    programme = employee['employee'][0]['programme']
    Objective.objects.create(
        branch=Branch.objects.get(id=branch),
        programme=Programme.objects.get(id=programme),
        framework=Framework.objects.latest('created'),
        objective=request.POST.get('objective', None),
        statement=request.POST.get('statement', None),
        baseline=request.POST.get('baseline', None),
        justification=request.POST.get('justification', None),
        link=request.POST.get('links', None)
    )
    return JsonResponse({"status": 200, "message": "Strategic Objective created successfully"})


def read_objective(request):
    employee = read_employee_info(request)
    branch = employee["employee"][0]['branch']
    objectives = Objective.objects.filter(branch_id=branch).values('branch_id', 'objective', 'id')
    objective = [obj for obj in objectives]
    return JsonResponse({"objectives": objective})


@login_required()
def create_imperative(request):
    Imperatives.objects.create(
        objective=Objective.objects.get(id=request.POST.get('obj_id')),
        link=request.POST.get('links', None)
    )
    return JsonResponse({"status": 200, "message": "Link to National Imperative created successfully"})


@login_required()
def create_subprogramme(request):
    employee = read_employee_info(request)
    programme = employee['employee'][0]['programme']
    sub = Subprogramme(
        subprogramme=request.POST.get('subprog', None),
        linked_programme=Programme.objects.get(id=programme)
    )
    sub.save()
    sub.objective.add(Objective.objects.get(id=request.POST.get('obj_id')))
    return JsonResponse({"status": 200, "message": "Subprogramme created successfully"})


@login_required()
def create_strategic_output(request):
    StrategicOutput.objects.create(
        objective=Objective.objects.get(id=request.POST.get('obj_id')),
        output=request.POST.get('output')
    )
    return JsonResponse({"status": 200, "message": "Strategic Objective created successfully"})


@login_required()
def create_kpi(request):
    KeyPerformanceIndicator.objects.create(
        objective=Objective.objects.get(id=request.POST.get('obj_id')),
        kpi=request.POST.get('kpi', None)
    )
    return JsonResponse({"status": 200, "message": "KPI created successfully"})


@login_required()
def read_kpi(request):
    employee = read_employee_info(request)
    branch = employee["employee"][0]['branch']
    kpis_object = KeyPerformanceIndicator.objects.filter(output__objective__branch=branch).values('kpi', 'id')
    # TODO optimise the above query
    kpis = [obj for obj in kpis_object]
    return JsonResponse({"kpis": kpis})


@login_required()
def create_target(request):

    start = request.POST.get('start_date', None)
    end = request.POST.get('start_date', None)
    start_date = end_date = ""
    if start:
        start_date = datetime.strptime(start, "%d/%m/%Y")
        start_date = datetime.strftime(start_date, '%Y-%m-%d')
    if start:
        end = datetime.strptime(end, "%d/%m/%Y")
        end_date = datetime.strftime(end, '%Y-%m-%d')

    AnnualTarget.objects.create(
        kpi=KeyPerformanceIndicator.objects.get(id=request.POST['kpi']),
        framework=Framework.objects.latest('created'),
        baseline=request.POST.get('baseline', None),
        evidence=request.POST.get('evidence', None),
        year_index=request.POST.get('year_index', None),
        timeframe_start_d=start_date,
        timeframe_end_d=end_date,
    )
    return JsonResponse({"status": 200, "message": "Target created successfully"})


@login_required()
def create_risk(request):
    employee = read_employee_info(request)
    branch = employee["employee"][0]['branch']
    Risk.objects.create(
        framework=Framework.objects.latest('created'),
        branch=Branch.objects.get(id=branch),
        desc=request.POST.get('desc', None),
        likelihood=request.POST.get('likelihood', None),
        mit_plan=request.POST.get('mit_plan', None),
        impact=request.POST.get('impact', None),
    )
    return JsonResponse({"status": 200, "message": "Risk created successfully"})


@login_required()
def create_resource_plan(request):
    ResourcePlan.objects.create(
        framework=Framework.objects.latest('created'),
        plan=request.POST.get('plan', None)
    )
    return JsonResponse({"status": 200, "message": "Resource Plan saved successfully"})
