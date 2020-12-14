from django.contrib import admin

from .models import Project, ProjectType, Status


class ProjectAdmin(admin.ModelAdmin):

    fields = ['organisation', 'programme', 'branch', 'component', 'name', 'project_manager', 'start_date', 'end_date',
              'project_type', 'budget', 'report_cycle', 'risk', 'number',
              'status', 'is_active', 'sponsor', 'comments', 'details']


admin.site.register(Project, ProjectAdmin)


class ProjectTypeAdmin(admin.ModelAdmin):

    fields = ['name']


admin.site.register(ProjectType, ProjectTypeAdmin)


class StatusAdmin(admin.ModelAdmin):

    fields = ['name']


admin.site.register(Status, StatusAdmin)

