from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Composter


class ComposterAdmin(UserAdmin):
    list_display = ('Email', 'OrganizationName', 'CommunityName', 'PhoneNumber', 'Location','is_staff')
    search_fields = ('Email', 'OrganizationName', 'CommunityName', 'PhoneNumber')
    ordering = ('Email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('Email', 'password')}),
        ('Personal Info', {'fields': ('OrganizationName', 'CommunityName', 'PhoneNumber')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('Email', 'OrganizationName', 'CommunityName', 'PhoneNumber', 'password1', 'password2'),
        }),
    )


admin.site.register(Composter, ComposterAdmin)