from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import EPMUser, Employee, Token, SalaryNotch, Supervisor


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = EPMUser
        fields = ('email', 'employee_code')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = EPMUser
        fields = ('email', 'password', 'employee_code', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'employee_code', 'is_admin', 'last_login', 'date_joined')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('employee_code', 'last_login',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Authentication', {'fields': ('token',)}),
        ('Date Joined', {'fields': ('date_joined',)}),

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'employee_code', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(EPMUser, UserAdmin)
# Now register the new UserAdmin...
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


class TokensAdmin(admin.ModelAdmin):
    list_display = ('token', 'token_is_used',)
    list_filter = ('token_is_used',)
    fieldsets = (

        ('Authentication', {'fields': ('token', 'token_is_used', 'expiry_date')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('token', 'token_is_used',)}
         ),
    )
    search_fields = ('token_is_used',)
    ordering = ('token_is_used',)
    filter_horizontal = ()


admin.site.register(Token, TokensAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    fields = ['user', 'department', 'job_title', 'date_of_birth', 'gender', 'title', 'first_name', 'last_name',
              'is_first_login', 'emp_status', 'race', 'disability_status', 'salary_notch', 'salary_level',
              'is_supervisor', 'organisation', 'programme', 'branch', 'component'
              ]


admin.site.register(Employee, EmployeeAdmin)


class SalaryNotchAdmin(admin.ModelAdmin):
    fields = ['duration', 'notch', 'part_time', 'full_time']


admin.site.register(SalaryNotch, SalaryNotchAdmin)


class SupervisorAdmin(admin.ModelAdmin):
    fields = ['name', 'is_active', 'employees']


admin.site.register(Supervisor, SupervisorAdmin)
