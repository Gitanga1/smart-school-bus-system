from django.contrib import admin
from .models import BusLocation, StudentAttendance

@admin.register(BusLocation)
class BusLocationAdmin(admin.ModelAdmin):
    list_display = ('bus', 'latitude', 'longitude', 'speed', 'timestamp')
    list_filter = ('bus', 'timestamp')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'bus', 'date', 'status', 'boarded_time', 'exited_time')
    list_filter = ('status', 'date', 'bus')
    search_fields = ('student__first_name', 'student__last_name')
    date_hierarchy = 'date'