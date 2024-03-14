from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Location
# from .models import AppUser
from .models import Event

# Register your models here.

# admin.site.register(Location)
# admin.site.register(AppUser)
# admin.site.register(Event)
admin.site.unregister(Group)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'zip_code', 'phone_number', 'website', 'email', "owner"  )
    ordering = ("name",)
    search_fields = ("name", "address")


# @admin.register(AppUser)
# class AppUserAdmin(admin.ModelAdmin):
#     list_display = (AppUser.__str__ , 'email', )
#     # list_display = ('first_name','last_name', 'email', )
#     ordering = ("first_name", "last_name")
#     search_fields = ("first_name", "last_name")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (("name", "location"), "event_date", "description", "manager", "approved")
    list_display = ('name', 'event_date', 'location', 'manager', )
    list_filter = ('event_date', "location")
    ordering = ("-event_date",)
    search_fields = ("name", "location")