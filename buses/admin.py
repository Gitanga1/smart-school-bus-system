from django.contrib import admin
from .models import Bus, DriverAssignment

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'license_plate', 'capacity', 'current_driver', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('bus_number', 'license_plate')

@admin.register(DriverAssignment)
class DriverAssignmentAdmin(admin.ModelAdmin):
    list_display = ('bus', 'driver', 'assigned_date', 'is_active')
    list_filter = ('is_active', 'assigned_date')