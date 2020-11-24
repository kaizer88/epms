from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from decimal import InvalidOperation
from .models import CurrentPayments, PaymentsCapitalAssets, TransfersSubsidies


@login_required()
def create_current_payments(requests):

    try:

        CurrentPayments.objects.create(
            compensation_employees=requests.POST['compensation']
        )
        return JsonResponse({
            "status": 200,
            "message": "Current payment saved successfully",
        })
    except ValidationError:
        return JsonResponse({
            "status": 52,
            "message": "Error saving compensation. Provide a valid decimal value",
        })

    except InvalidOperation:
        return JsonResponse({
            "status": 52,
            "message": "Error saving capital assets. Maximum decimal places is 2 and length is 10 digits",
        })


@login_required()
def create_capital_assets(requests):
    try:

        PaymentsCapitalAssets.objects.create(
            fixed_accounts=requests.POST['accounts'],
            intangible_assets=requests.POST['assets'],
            machinery=requests.POST['machinery']
        )
        return JsonResponse({
            "status": 200,
            "message": "Capital assets saved successfully",
        })
    except ValidationError:
        return JsonResponse({
            "status": 52,
            "message": "Error saving capital assets. Provide a valid decimal value",
        })
    except InvalidOperation:
        return JsonResponse({
            "status": 52,
            "message": "Error saving capital assets. Maximum decimal places is 2 and length is 10 digits",
        })


@login_required()
def create_transfers(requests):
    try:

        TransfersSubsidies.objects.create(
            dept_agencies=requests.POST['agencies'],
            social_benefits=requests.POST['benefits'],
            non_profit_inst=requests.POST['institutes']
        )
        return JsonResponse({
            "status": 200,
            "message": "Capital assets saved successfully",
        })
    except ValidationError:
        return JsonResponse({
            "status": 52,
            "message": "Error saving capital assets. Provide a valid decimal value",
        })
    except InvalidOperation:
        return JsonResponse({
            "status": 52,
            "message": "Error saving capital assets. Maximum decimal places is 2 and length is 10 digits",
        })

