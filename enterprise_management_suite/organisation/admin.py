from django.contrib import admin
from .models import Organisation, Branch, Component, Programme, FinancialYear


class ComponentAdmin(admin.ModelAdmin):

    fields = ['organisation', 'name']


admin.site.register(Component, ComponentAdmin)


class BranchAdmin(admin.ModelAdmin):

    fields = ['component', 'name']


admin.site.register(Branch, BranchAdmin)


class OrganisationAdmin(admin.ModelAdmin):

    fields = ['name', 'logo']


admin.site.register(Organisation, OrganisationAdmin)

#
# class SubProgrammeAdmin(admin.ModelAdmin):
#
#     fields = ['programme', 'name', 'purpose', 'index_no']


# admin.site.register(SubProgramme, SubProgrammeAdmin)


class ProgrammeAdmin(admin.ModelAdmin):

    fields = ['organisation', 'branch', 'name', 'purpose', 'index_no']


admin.site.register(Programme, ProgrammeAdmin)


class FinancialYearAdmin(admin.ModelAdmin):

    fields = ['org', 'financial_period_start', 'financial_period_end', 'year', 'active']


admin.site.register(FinancialYear, FinancialYearAdmin)
