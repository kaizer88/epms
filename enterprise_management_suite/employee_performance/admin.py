from django.contrib import admin

from .models import KRAReview, MOReview, KeyResultArea, MeasurableOutput, Bathopele,  GenericSTD, \
    CoreManagementCriteria, TrainingNeed, PerformanceAgreement, ReviewPeriod, KeyPerformanceIndicator, Target, \
    ProcessedKRAReview


class OutputsReviewAdmin(admin.ModelAdmin):
    fields = ['reviewed_kra_id', 'pa_weight', 'self_rating', 'agreed_rating', 'final_score', 'self_comment',
              'super_comment', 'self_note', 'super_note', 'rev_weight', 'employee_has_signed', 'supervisor_has_signed']


admin.site.register(MOReview, OutputsReviewAdmin)


class ReviewPeriodAdmin(admin.ModelAdmin):
    fields = ['period_start', 'period_end', 'cycle']


admin.site.register(ReviewPeriod, ReviewPeriodAdmin)


class KRAReviewAdmin(admin.ModelAdmin):
    fields = ['employee', 'supervisor', 'kra_id', 'dispute', 'outputs',
              'super_rating', 'final_score', 'self_rating', 'agreed_rating', 'rev_weight']


admin.site.register(KRAReview, KRAReviewAdmin)


class KRAAdmin(admin.ModelAdmin):

    fields = ['review', 'kra_id', 'kra_pa_id', 'supervisor', 'employee', 'kra', 'self_weight', 'outputs', 'bathophele',
              'evidence', 'is_active']


admin.site.register(KeyResultArea, KRAAdmin)


class OutputAdmin(admin.ModelAdmin):

    fields = ['output', 'mo_kra_id', 'output_id', 'slug', 'target', 'resources', 'cal_date', 'time_frame', 'self_weight',
              'super_weight', 'self_rating', 'super_rating', 'agreed_rating']
    prepopulated_fields = {'slug': ('output',)}


admin.site.register(MeasurableOutput, OutputAdmin)


class BathopeleAdmin(admin.ModelAdmin):

    fields = ['description', 'slug']
    prepopulated_fields = {'slug': ('description',)}


admin.site.register(Bathopele, BathopeleAdmin)


class GenericSTDAdmin(admin.ModelAdmin):

    fields = ['description', 'weight']


admin.site.register(GenericSTD, GenericSTDAdmin)


class CMCAdmin(admin.ModelAdmin):
    fields = ['bophele', 'g_std', 'description', 'weight', 'dept_specific']


admin.site.register(CoreManagementCriteria, CMCAdmin)


class PAAdmin(admin.ModelAdmin):
    fields = ['pa_id', 'employee', 'supervisor', 'kras', 'employee_has_signed', 'supervisor_has_signed',
              'period_start', 'period_end', 'fyear', 'is_active']


admin.site.register(PerformanceAgreement, PAAdmin)


class TrainingNeedsAdmin(admin.ModelAdmin):
    fields = ['pdp_kra_id', 'pdp_id', 't_type', 'outcome', 'time_frame', 'is_active']


admin.site.register(TrainingNeed, TrainingNeedsAdmin)


class KPIAdmin(admin.ModelAdmin):
    filter = ['description', 'staff_weight']


admin.site.register(KeyPerformanceIndicator, KPIAdmin)


class TargetAdmin(admin.ModelAdmin):
    filter = ['description', 'start_date', 'end_date']


admin.site.register(Target, TargetAdmin)


class ProcessedKRAReviewAdmin(admin.ModelAdmin):
    fields = ['review_type', 'review', 'processed_rev_id', 'period_start', 'period_end', 'employee_has_signed',
              'supervisor_has_signed', 'email_is_sent']


admin.site.register(ProcessedKRAReview, ProcessedKRAReviewAdmin)
