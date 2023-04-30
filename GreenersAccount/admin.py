from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Greener


class GreenerAdmin(UserAdmin):
    list_display = ('id', 'FirstName', 'LastName', 'Email', 'PhoneNumber', 'composter')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('FirstName', 'LastName', 'Email', 'PhoneNumber')
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('FirstName', 'LastName', 'Email', 'password', 'PhoneNumber')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Composter', {'fields': ('composter',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('FirstName', 'LastName', 'Email', 'password1', 'password2', 'PhoneNumber', 'composter', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
         ),
    )


admin.site.register(Greener, GreenerAdmin)
