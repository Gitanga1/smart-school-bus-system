from django.contrib import admin
from .models import Student, StudentBusAssignment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'grade', 'parent')
    list_filter = ('grade',)
    search_fields = ('first_name', 'last_name', 'student_id')

@admin.register(StudentBusAssignment)
class StudentBusAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'bus', 'assigned_date', 'is_active')
    list_filter = ('is_active', 'assigned_date')