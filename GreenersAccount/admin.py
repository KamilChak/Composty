from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Greener, Offer


class GreenerAdmin(UserAdmin):
    list_display = ('id', 'FirstName', 'LastName', 'Email', 'PhoneNumber', 'composter', 'Location', 'wallet', 'ComposterStatus')
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

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'manure', 'brown_material', 'green_material', 'date_range_start', 'date_range_end', 'confirmed')