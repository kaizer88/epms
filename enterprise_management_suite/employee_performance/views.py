import uuid
from datetime import datetime, date

<<<<<<< HEAD
# from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
# from django.shortcuts import render, redirect, render_to_response, get_object_or_404
=======
from django.shortcuts import render
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
>>>>>>> master
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import KRAReview, KeyResultArea, PerformanceAgreement, MeasurableOutput, TrainingNeed, ReviewPeriod, \
    KeyPerformanceIndicator, Target, ProcessedKRAReview
from accounts.models import Employee, Supervisor, EPMUser
<<<<<<< HEAD
from .forms import PAForm
=======
>>>>>>> master
# from .forms import ReviewForm, PAForm
from organisation.models import FinancialYear


@login_required(login_url='/')
def financial_year(request):

    try:
        employee = Employee.objects.select_related('user').get(user=request.user)
    except ObjectDoesNotExist:
        # TODO add logging. This is unlikely to happen except for a case where users data is not properly loaded yet
        return JsonResponse({'status': 51, 'message': 'Internal server. Report to administrator'})
    else:
        # TODO cater for prev years in future?
        finance = FinancialYear.objects.get(org=employee.organisation, active=True)
        return JsonResponse({'status': 200, 'message': finance.year})


@login_required(login_url='/')
def create_agreement(request):

    if not PerformanceAgreement.objects.filter(employee=request.user.employee, is_active=True):
        pa_id = uuid.uuid4()
        start = datetime.strptime(request.POST['period_start'], '%d/%m/%Y') if request.POST['period_start'] is not ''\
            else None
        end = datetime.strptime(request.POST['period_end'], '%d/%m/%Y') if request.POST['period_end'] is not '' \
            else None
        selected_superv = request.POST.get('superv', None)
        pa = PerformanceAgreement(
            pa_id=pa_id,
            period_start=str(datetime.strftime(start, '%Y-%m-%d')) if start is not None else '',
            period_end=str(datetime.strftime(end, '%Y-%m-%d')) if end is not None else '',
            fyear=request.POST['fin_year'],
        )
        pa.save()
        pa.employee.add(request.user.employee)
        if selected_superv:
            superv_emp_code = selected_superv.split(" ")[0]
            supervisor = Supervisor.objects.get(name__user=superv_emp_code)
            pa.supervisor.add(supervisor)
        return JsonResponse({"status": 200, "message": "Performance Agreement Created Successfully."})

    return JsonResponse({'status': 52, "message": "Failed to save new record. You have an active Performance Agreement"})


@login_required(login_url='/')
def get_user_pa(request):

    pa = PerformanceAgreement.objects.filter(employee=request.user.employee).values()
    pa_id = [_id for _id in pa]
    return JsonResponse({'pa': pa_id[0]['pa_id']})


def pa_update(request):
    pass


@login_required(login_url='/')
def create_kra(request):
    if request.method == 'POST':
        weight = request.POST['self_weight'] if request.POST['self_weight'] != "" else 0
        try:
            kra = KeyResultArea(
                self_weight=weight,
                kra=request.POST['kra'],
                kra_pa_id=request.POST['pa_id'],
                kra_id=uuid.uuid4()
            )
            kra.save()
            kra.employee.add(request.user.employee)
            pa = PerformanceAgreement.objects.latest('created')
            pa.kras.add(kra)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 52, 'message': 'Failed to save record Internal Server Error Occurred'})
        else:
            return JsonResponse({'status': 200, 'message': "KRA added successfully"})


@login_required(login_url='/')
def create_target(request):

    if request.method == 'POST':
        try:
            target = Target(
                target_id=uuid.uuid4(),
                kpi_id=request.POST['kpi_id'],
                target=request.POST['target'],
                evidence=request.POST['evidence'],
                baseline=request.POST['baseline'],
            )
            target.save()
        except ValidationError:
            return JsonResponse({'status': 52, 'message': 'Failed to save new Target'})
        kpi = KeyPerformanceIndicator.objects.get(kpi_id=request.POST['kpi_id'])
        try:
            kpi.target.add(target)
            return JsonResponse({'status': 200, 'message': 'Target added successfully'})
        except Exception:
            return JsonResponse({'status': 52, 'message': 'Failed to save new Target'})


@login_required(login_url='/')
def create_measurable_output(request):
    if request.method == 'POST':
        calendar_date = request.POST.get('cal_date', None)
        d = ''
        if calendar_date:
            d = datetime.strptime(calendar_date, "%d/%m/%Y")
            d = datetime.strftime(d, '%Y-%m-%d')
        time_frame = request.POST.get('time_frame', 'default')
        try:
            mo = MeasurableOutput(
                self_weight=request.POST['self_weight'],
                mo_kra_id=request.POST['mo_kra_id'],
                output=request.POST['output'],
                time_frame=time_frame if time_frame != 'default' else None,
                resources=request.POST['resources'],
                cal_date=d if d is not '' else None,
                output_id=uuid.uuid4(),
                target=request.POST['target']
            )
            mo.save()
            kra = KeyResultArea.objects.get(kra_id=request.POST['mo_kra_id'])
            kra.outputs.add(mo)
        except Exception as e:
            return JsonResponse({'status': 52, 'message': 'Failed to save new Measurable Output'})
        else:
            return JsonResponse({'status': 200, 'message': 'Measurable Output added successfully'})


@login_required(login_url='/')
def create_key_performance_indicator(request):
    if request.method == 'POST':
        if request.POST.get('kra_id', None):
            try:
                kpi = KeyPerformanceIndicator(
                    kpi_id=uuid.uuid4(),
                    description=request.POST.get('kpi', None),
                    staff_weight=request.POST.get('weight', None),
                    )
                kpi.save()
                kra = KeyResultArea.objects.get(kra_id=request.POST.get('kra_id'))
                kra.indicators.add(kpi)
                return JsonResponse({'status': 200, 'message': 'KPI added successfully'})
            except ValidationError as e:
                return JsonResponse({'status': 52, 'message': 'Failed to save new KPI {}'.format(e)})
        return JsonResponse({'status': 52, 'message': 'Failed to process. Please select KRA'})


@login_required(login_url='/')
def list_key_performance_indicator(request):
    indicator_obj = KeyPerformanceIndicator.objects.filter(keyresultarea__employee=request.user.employee).values()
    indicators = [i for i in indicator_obj]
    if indicators:
        return JsonResponse({'indicators': indicators})
    return JsonResponse({"status": 40, "message": "No KPI found"})


@login_required(login_url='/')
def get_indicator(request):
    _id = request.GET['kpi_id']
    kpis_list = KeyPerformanceIndicator.objects.filter(kpi_id=_id).values('description', 'kpi_id', 'kpi', 'staff_weight')
    kpis = [i for i in kpis_list]
    if kpis:
        return JsonResponse({'kpis': kpis})
    return JsonResponse({"status": 40, "message": "No KPI found"})


@login_required(login_url='/')
def delete_indicator(request):

    KeyPerformanceIndicator.objects.filter(kpi_id=request.POST['id']).delete()
    return JsonResponse({'status': 200, 'message': 'KPI Deleted Successfully'})


# TODO deprecated
@login_required(login_url='/')
def list_measurable_outputs(request):
    outputs = MeasurableOutput.objects.filter(keyresultarea__employee=request.user.employee, is_active=True).values()
    outputs_list = [kra for kra in outputs]
    return JsonResponse({'outputs': outputs_list})


def list_targets(request):
    targets = Target.objects.all().values()
    targets_list = [item for item in targets]
    return JsonResponse({'targets': targets_list})


@login_required(login_url='/')
def get_measurable_output(request):

    output = MeasurableOutput.objects.filter(keyresultarea__employee=request.user.employee, is_active=True,
                                             output_id=request.GET['output_id']).values()

    output_fields = [field for field in output]
    return JsonResponse({'output': output_fields})


@login_required(login_url='/')
def update_mo(request):

    calendar_date = request.POST.get('cal_date', None)
    _date = ''
    if calendar_date:
        _date = datetime.strptime(calendar_date, "%d/%m/%Y")
        _date = datetime.strftime(_date, '%Y-%m-%d')
    time_frame = request.POST.get('tf', 'default')

    try:
        MeasurableOutput.objects.filter(output_id=request.POST['_id']).update(
            output=request.POST['output'],
            self_weight=request.POST['emp_weight'],
            resources=request.POST['rsc'],
            cal_date=_date if _date is not '' else None,
            time_frame=time_frame if time_frame != 'default' else None,
        )

    except Exception as e:
        print("error occurred due to : {}".format(e))
        return JsonResponse({'results': 'ok',
                             'msg': 'Updating Output failed'})
    else:
        return JsonResponse({'results': 'ok',
                             'msg': 'Output updated successfully'
                             })


@login_required(login_url='/')
def delete_mo(request):

    try:
        MeasurableOutput.objects.filter(output_id=request.POST['id']).update(
            is_active=False
        )
    except Exception as e:
        return JsonResponse({'status': 51,
                            'message': 'Error Occurred. Failed to delete Measurable Output'})
    else:
        return JsonResponse({'status': 200,
                             'message': 'Output Deleted Successfully'})


@login_required(login_url='/')
def create_pdp(request):

    _id = uuid.uuid4()
    try:
        pdp = TrainingNeed.objects.create(
            t_type=request.POST['t_type'],
            outcome=request.POST['outcome'],
            time_frame=request.POST['frame'],
            pdp_id=_id,
            pdp_kra_id=request.POST['kra_id'],
            is_active=True
        )
        pdp.save()
        kra = KeyResultArea.objects.get(kra_id=request.POST['kra_id'])
        kra.training_needs.add(pdp)
        out = request.POST['outcome']
        content = (out[:40] + '...') if len(out) > 10 else out
        return JsonResponse({'results': 'ok',
                             'message': 'PDP added successfully',
                             'content': content,
                             'pdp': _id})

    except Exception as e:
        print("error occurred to: {}".format(e))
        return JsonResponse({'results': 'Server Error Occurred'})


@login_required(login_url='/')
def update_pdp(request):
    try:
        pdp = TrainingNeed.objects.filter(pdp_id=request.POST['pdp_id']).update(
            t_type=request.POST['t_type'],
            outcome=request.POST['outcome'],
            time_frame=request.POST['frame'],
        )
        print(type(pdp))
        pdp.save()
        return JsonResponse({'results': 'ok',
                             'message': 'PDP updated successfully'
                             })
    except Exception as e:
        print("error occurred due to:{}".format(e))
        return JsonResponse({'results': 'error',
                             'message': 'Server Error Occurred',
                             })


@login_required(login_url='/')
def load_pdp(request):
    try:
        pdp_list = TrainingNeed.objects.filter(pdp_id=request.GET['pdp_id'], is_active=True).values()
        pdp = [pdp for pdp in pdp_list]
        return JsonResponse({'results': 'ok',
                             'message': 'Loading PDP {}'.format(pdp),
                             'obj': pdp
                             })
    except Exception as e:
        print("error occurred due to:{}".format(e))
        return JsonResponse({'results': 'Server Error Occurred'})


@login_required(login_url='/')
def list_training_needs(request):
    try:
        pdp_list = TrainingNeed.objects.filter(keyresultarea__employee=request.user.employee, is_active=True).values()
        pdp = [pdp for pdp in pdp_list]
        return JsonResponse({'results': 'ok',
                             'message': 'Loading PDP {}'.format(pdp),
                             'obj': pdp
                             })
    except Exception as e:
        print("error occurred due to:{}".format(e))
        return JsonResponse({'results': 'Server Error Occurred'})


@login_required(login_url='/')
def delete_pdp(request):
    try:
        pdp = TrainingNeed.objects.filter(pdp_id=request.POST['pdp_id']).update(
            is_active=False
        )

        # pdp.save()
        return JsonResponse({'results': 'ok',
                             'message': 'PDP deleted successfully'
                             })
    except Exception as e:
        print("error occurred due to:{}".format(e))
        return JsonResponse({'results': 'fail',
                             'message':  'Server Error Occurred'
                             })


@login_required(login_url='/')
def sign_agreement(request):

    if request.user.employee.is_supervisor:
        superv = Supervisor.objects.get(name=request.user.employee)
        if PerformanceAgreement.objects.filter(supervisor=superv, supervisor_has_signed=False, is_active=True,
                                               employee_has_signed=True, pa_id='7e0cce2cdc21453e8bdf4cb9fd8b8c89'
                                               ):
                PerformanceAgreement.objects.update(supervisor_has_signed=True)
                # TODO send notification to supervisor and this employees inbox
                return JsonResponse({"status": 200, "message": "Agreement has been signed successfully."})
        else:
            return JsonResponse({"status": 52, "message": "Failed to sign agreement"})
    elif PerformanceAgreement.objects.filter(employee=request.user.employee, supervisor_has_signed=False,
                                             employee_has_signed=False,
                                             is_active=True, pa_id='7e0cce2cdc21453e8bdf4cb9fd8b8c89'
                                             ):
        PerformanceAgreement.objects.update(employee_has_signed=True)
        # TODO send notification to supervisor and this employees inbox
        return JsonResponse({"status": 200, "message": "Agreement has been signed successfully."})
    else:
        return JsonResponse({"status": 52, "message": "Failed to sign agreement"})


def get_pa_sum(request):
    pass


@login_required(login_url='/')
def fetch_kra(request):

    kras = KeyResultArea.objects.select_related().filter(employee=request.user.employee, kra_id=request.GET['kra_id'],
                                                         is_active=True).values('kra', 'self_weight',
                                                                                'supervisor__name__first_name',
                                                                                'supervisor__name__last_name',
                                                                                'supervisor__name__user__employee_code',
                                                                                'kra_id'
                                                                                )
    kra_fields = [field for field in kras]
    return JsonResponse({'kra': kra_fields})


@login_required(login_url='/')
def update_kra(request):

    kra = KeyResultArea.objects.get(kra_id=request.POST['kra_id'])
    kra.kra = request.POST['kra']
    kra.self_weight = request.POST['self_weight']
    kra.save()
    return JsonResponse({'status': 200, 'message': 'KRA updated successfully'})


def delete_kra(request):

    try:
        KeyResultArea.objects.filter(employee=request.user.employee, kra_id=request.POST['kra_id']).update(
            is_active=False
        )
    except Exception:
        print(Exception)
        return JsonResponse({'error': 'Database Error.'})

    else:
        return JsonResponse({'ok': 'KRA Deleted Successfully',
                             'results': 'ok'
                             })


@login_required(login_url='/')
def list_kras(request):

    kras = KeyResultArea.objects.select_related().filter(employee=request.user.employee, is_active=True).values(
        'self_weight',
        'kra',
        'kra_id',
    )
    kra_list = [kra for kra in kras]
    if len(kra_list) > 0:
        return JsonResponse({
            'status': 200,
            'message': 'Loading KRAs',
            'kras': kra_list
        })
    else:
        return JsonResponse({'status': 51, 'message': 'You do not have any KRAs'})


@login_required(login_url='/')
def get_review_kra(request):

    kras = KeyResultArea.objects.select_related().filter(employee=request.user.employee, is_active=True).values(
        'self_weight',
        'kra',
        'kra_id',
        'review__self_rating'
    )
    kra_list = [kra for kra in kras]
    if len(kra_list) > 0:
        return JsonResponse({
            'status': 200,
            'message': 'Key Result Areas',
            'kras': kra_list,
        })
    else:
        return JsonResponse({'status': 51, 'message': 'You do not have any Key Result Areas'})


def review_update_old(request):

    template = 'employee_performance/start_review.html'
    emp_review = KRAReview.objects.get(employee__user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES or None, instance=emp_review)
        if form.is_valid():
            if request.POST['is_signed']:
                email_supervisor(request)
                update_notification_status(request)
        form.save()
        return redirect('/dashboard/')
    else:
        form = ReviewForm(instance=emp_review)
    return render(request, template, {'review': form})


@login_required(login_url='/')
def save_review_form(request, form, template_name):
    data = {}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required(login_url='/')
def review_create(request):
    data = {}
    # if request.method == 'POST':
    #     emp_review = Review.objects.get(employee__user=request.user)
    #     form = ReviewForm(request.POST, request.FILES or None, instance=emp_review)
    #     if form.is_valid():
    #         form.save()
    #         data['form_is_valid'] = True
    #     else:
    #         data['form_is_valid'] = False
    #         print(form.errors)
    # else:

        # form = ReviewForm()

    kras = KeyResultArea.objects.select_related().values('created')  #add filter
    kras_list = [kra for kra in kras]
    context = {'kras': kras_list}
    data['html_form'] = render_to_string('employee_performance/epr/start_review.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(data)


@login_required(login_url='/')
def review_update(request, pk):
    book = get_object_or_404(KRAReview, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=book)
    else:
        form = ReviewForm(instance=book)
    return save_review_form(request, form, 'employee_performance/epr/start_review.html')


@login_required(login_url='/')
def review_periods(request):

    period = ReviewPeriod.objects.values()  # add filter to get those created by the supervisor of this curr empl
    per = [q for q in period]
    # print(x.strftime('%b'))
    return JsonResponse({'per': per})


@login_required(login_url='/')
def save_employee_kra_rating(request):

    emp = Employee.objects.get(user=request.user)
    rev = KRAReview.objects.update_or_create(
        kra_id=request.POST['kra_id'],
        defaults={'self_rating': request.POST['self_rating'],
                  'employee': emp,
                  }
            )
    KeyResultArea.objects.filter(kra_id=request.POST['kra_id']).update(review=rev[0])
    return JsonResponse({'status': 200, 'message': 'Weight Saved Successfully'})


@login_required(login_url='/')
def save_bulk_review(request):
    kra_list = ('7061c75057a149c0aaa33ca6d5a60b9d', '7b04bfa23ec24e28bedab7fe93d9c38b')

    start = datetime.strptime(request.POST['period_start'], '%d/%m/%Y') if request.POST['period_start'] is not '' \
        else None
    end = datetime.strptime(request.POST['period_end'], '%d/%m/%Y') if request.POST['period_end'] is not '' \
        else None

    rev_obj = ProcessedKRAReview.objects.create(
        processed_rev_id=uuid.uuid4(),
        review_type=request.POST['rev_type'],
        period_start=str(datetime.strftime(start, '%Y-%m-%d')) if start is not None else '',
        period_end=str(datetime.strftime(end, '%Y-%m-%d')) if end is not None else '',
        employee_has_signed=True,

        )
    for i in kra_list:
        print(i)
        kra = KRAReview.objects.get(kra_id=i)
        rev_obj.review.add(kra)
        print(True)

def email_supervisor(request):
    """
    Sends notification to supervisor
    :param request:
    :return:
    """

    emp_super_v = Supervisor.objects.select_related('employee').get(employees__user=request.user)
    send_mail(
        'Confirmation',
        'Please confirm if you are a supervisor to: {} {}. \nPERSAL Number: {} \nRole: {}'.format(
                                            request.user.employee.first_name,
                                            request.user.employee.last_name,
                                            request.user.employee_code,
                                            request.user.employee.role,
                                         ),
        'admin@avortech.co.za',
        [emp_super_v.employee.user.email],
    )


def update_notification_status(request):  # test
    notice = KRAReview.objects.get(employee__user__employee_code=request.user)
    notice.email_is_sent = True
    notice.save()


@login_required
def confirm_employee(request, persal):

    template = 'employee_performance/confirm_employee.html'
    if request.method == 'POST':
        KRAReview.objects.filter(employee__user__employee_code=persal).update(
            is_confirmed=True
        )
        return redirect('/dashboard')
    return render(request, template)

