from django.contrib import admin

# Register your models here.

from .models import Overview, Goal, Framework, Objective, Imperatives, StrategicOutput, KeyPerformanceIndicator, \
    AnnualTarget, Risk, ResourcePlan, Subprogramme

class OverviewAdmin(admin.ModelAdmin):

    fields = ['is_signed', 'signed_user', 'vision', 'mission', 'values', 'revisions', 'mtef_budget', 'priority_programme', 'goals', 'analysis',
              'risks']


admin.site.register(Overview, OverviewAdmin)


class GoalAdmin(admin.ModelAdmin):

    fields = ['goal_id', 'goal', 'statement']


admin.site.register(Goal, GoalAdmin)


class FrameworkAdmin(admin.ModelAdmin):

    fields = ['branch', 'obj_id', 'year']


admin.site.register(Framework, FrameworkAdmin)


class ObjectivesAdmin(admin.ModelAdmin):

    fields = ['programme', 'strategic_outputs', 'branch', 'framework', 'objective', 'baseline', 'justification', 'link', 'statement',
              'index_no']


admin.site.register(Objective, ObjectivesAdmin)


class ImperativesAdmin(admin.ModelAdmin):

    fields = ['link', 'objective']


admin.site.register(Imperatives, ImperativesAdmin)


class SubprogrammesAdmin(admin.ModelAdmin):

    fields = ['linked_programme', 'purpose', 'index_no', 'subprogramme', 'objective']


admin.site.register(Subprogramme, SubprogrammesAdmin)


class StrategicOutputAdmin(admin.ModelAdmin):

    fields = ['kpis', 'output']


admin.site.register(StrategicOutput, StrategicOutputAdmin)


class KPIAdmin(admin.ModelAdmin):

    fields = ['annual_targets', 'kpi']


admin.site.register(KeyPerformanceIndicator, KPIAdmin)


class AnnualTargetAdmin(admin.ModelAdmin):

    fields = ['framework', 'baseline', 'evidence', 'year_index', 'timeframe_start_d', 'timeframe_end_d']


admin.site.register(AnnualTarget, AnnualTargetAdmin)


class RiskAdmin(admin.ModelAdmin):

    fields = ['branch', 'framework', 'desc', 'likelihood', 'impact', 'mit_plan']


admin.site.register(Risk, RiskAdmin)


class ResourcePlanAdmin(admin.ModelAdmin):

    fields = ['framework', 'plan']


admin.site.register(ResourcePlan, ResourcePlanAdmin)
