from django.contrib import admin
from .models import SystemStats

@admin.register(SystemStats)
class SystemStatsAdmin(admin.ModelAdmin):
    list_display = ('total_buses', 'active_buses', 'total_students', 'active_routes', 'students_transported_today', 'last_updated')
    readonly_fields = ('last_updated',)