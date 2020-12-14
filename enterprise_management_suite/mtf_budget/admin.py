from django.contrib import admin

from .models import PaymentsCapitalAssets, TransfersSubsidies, CurrentPayments


class PaymentsCapitalAssetsAdmin(admin.ModelAdmin):

    fields = ['fixed_accounts', 'intangible_assets', 'machinery']


admin.site.register(PaymentsCapitalAssets, PaymentsCapitalAssetsAdmin)


class TransfersSubsidiesAdmin(admin.ModelAdmin):

    fields = ['dept_agencies', 'social_benefits', 'non_profit_inst']


admin.site.register(TransfersSubsidies, TransfersSubsidiesAdmin)


class CurrentPaymentsAdmin(admin.ModelAdmin):

    fields = ['compensation_employees']


admin.site.register(CurrentPayments, CurrentPaymentsAdmin)
