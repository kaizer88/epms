from django.contrib import admin

from .models import QuarterlyTarget, Risk


class QuarterlyTargetAdmin(admin.ModelAdmin):

    fields = ['subprogramme', 'objective', 'output', 'kpi', 'annual_target', 'start_date', 'end_date',
              'baseline', 'evidence'
              ]


admin.site.register(QuarterlyTarget, QuarterlyTargetAdmin)


class RiskAdmin(admin.ModelAdmin):

    fields = ['quarterly_target', 'description']


admin.site.register(Risk, RiskAdmin)
