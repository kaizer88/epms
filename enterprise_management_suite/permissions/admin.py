from django.contrib import admin

from .models import AccessLevel, Contributor, ActiveProjectAccessDetails, Signature


class AccessLevelAdmin(admin.ModelAdmin):

    fields = ['name', 'mode', 'description']


admin.site.register(AccessLevel, AccessLevelAdmin)


class ContributorAdmin(admin.ModelAdmin):

    fields = ['employee', 'project', 'queue_position', 'note']


admin.site.register(Contributor, ContributorAdmin)


class ActiveProjectAccessDetailsAdmin(admin.ModelAdmin):

    fields = ['contributor', 'access_level', 'project']


admin.site.register(ActiveProjectAccessDetails, ActiveProjectAccessDetailsAdmin)


class SignatureAdmin(admin.ModelAdmin):

    fields = ['project', 'token', 'contributor']


admin.site.register(Signature, SignatureAdmin)
