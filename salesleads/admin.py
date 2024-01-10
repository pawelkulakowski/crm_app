from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin

from salesleads.forms import ExportUserCreationForm

from salesleads.models import (
    Comment,
    ContactPerson,
    Country,
    ExportUser,
    SalesLead,
    PlannedActivities
)


class ExportUserAdmin(UserAdmin):
    model = ExportUser
    add_form = ExportUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User role',
            {
                'fields': ('market',)
            }
        )
    )


@admin.register(SalesLead)
class SalesLeadAdmin(OSMGeoAdmin):
    default_lon = 1836225
    default_lat = 6537059
    default_zoom = 6
    list_display = ('company_name', 'location', 'street', 'city', 'postcode', 'country')


admin.site.register(Comment)
admin.site.register(ContactPerson)
admin.site.register(Country)
admin.site.register(ExportUser, ExportUserAdmin)
admin.site.register(PlannedActivities)
