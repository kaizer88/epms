import uuid
import json
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from strategy.models import Overview, Framework, Objective, Subprogramme, StrategicOutput, KeyPerformanceIndicator, \
    AnnualTarget
from accounts.models import Employee

from .models import QuarterlyTarget, Risk


def get_employee_info(request):
    employee = Employee.objects.filter(user=request.user).values(
                                                                 'branch__name',
                                                                 'programme__name'
                                                                 )
    employee_data = [e for e in employee]

    return {"employee": employee_data}


@login_required()
def get_app_context(request):

    programme = request.user.employee.programme
    sub_programmes = Subprogramme.objects.filter(linked_programme=programme).values(
                                    'id',
                                    'subprogramme'
                                    )
    sub_programmes = [prog for prog in sub_programmes]
    info = get_employee_info(request)

    strategy = Overview.objects.filter().values(
        'vision', 'mission', 'analysis', 'mtef_budget', 'revisions', 'risks'
    )
    static_strategy = [i for i in strategy]

    return JsonResponse({
        "sub": sub_programmes,
        "info": info,
        "strat": static_strategy
    })


@login_required()
def get_objectives(request):

    sub_programmes = Subprogramme.objects.filter(id=request.GET.get("_id")).values(
        'id',
        'objective__objective',
        'objective__id'
    )
    objectives = [obj for obj in sub_programmes]
    return JsonResponse({
        "obj": objectives
    })


@login_required()
def get_outputs(request):

    outputs_object = StrategicOutput.objects.filter(objective=request.GET.get("_id")).values("output", "id")
    outputs = [out for out in outputs_object]
    return JsonResponse({
        "outputs": outputs
    })


@login_required()
def get_kpis(request):

    kpi_object = KeyPerformanceIndicator.objects.filter(strategicoutput=request.GET.get("_id")).values("kpi", "id")
    kpi_list = [kpi for kpi in kpi_object]
    return JsonResponse({
        "kpi": kpi_list
    })


@login_required()
def get_annual_targets(request):

    annual_targets = AnnualTarget.objects.filter(keyperformanceindicator=request.GET.get("_id")).values(
                                                                            "timeframe_start_d",
                                                                            "timeframe_end_d",
                                                                            "id"
                                                                        )
    targets = [t for t in annual_targets]
    return JsonResponse({
        "targets": targets
    })


@login_required()
def create_quarterly_targets(request):

    sub_programme = Subprogramme.objects.get(id=request.POST.get("subprog"))
    objective = Objective.objects.get(id=request.POST.get("objective"))
    output = StrategicOutput.objects.get(id=request.POST.get("output"))
    kpi = KeyPerformanceIndicator.objects.get(id=request.POST.get("kpi"))
    target = AnnualTarget.objects.get(id=request.POST.get("ann_target"))

    quarter = int(request.POST.get("quarter"))
    start = request.POST.get("start", None)
    end = request.POST.get("end", None)
    baseline = request.POST.get("baseline", None)
    evidence = request.POST.get("evidence", None)

    risks = json.loads(request.POST.get('risks'))
    quarterly_risks = risks['risks']
    start_date = end_date = ""
    if start:
        start_date = datetime.strptime(start, "%d/%m/%Y")
        start_date = datetime.strftime(start_date, '%Y-%m-%d')
    if end:
        end = datetime.strptime(end, "%d/%m/%Y")
        end_date = datetime.strftime(end, '%Y-%m-%d')
    quarter_uuid = uuid.uuid4()
    target = QuarterlyTarget(
        uuid=quarter_uuid,
        subprogramme=sub_programme,
        objective=objective,
        output=output,
        kpi=kpi,
        annual_target=target,
        start_date=start_date,
        end_date=end_date,
        baseline=baseline,
        evidence=evidence,
        quarter=quarter,

    )
    target.save()
    save_related_risks(quarterly_risks, target)

    return JsonResponse({
        "status": 200,
        "message": "Annual Performance Plan for Quarter: {} saved successfully".format(
            quarter
        )
    })


def save_related_risks(quarterly_risks, target):
    for i in range(len(quarterly_risks)):
        val = [d['risk'] for d in quarterly_risks][i]
        risk = Risk(description=val)
        risk.save()
        risk.quarterly_target.add(target)
