from django.db import models
from accounts.models import User

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    grade = models.CharField(max_length=10)
    parent = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'parent'})
    home_address = models.TextField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.grade})"
    
    class Meta:
        verbose_name_plural = "Students"

class StudentBusAssignment(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    bus = models.ForeignKey('buses.Bus', on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.student} -> Bus {self.bus.bus_number}"
    
    class Meta:
        verbose_name_plural = "Student Bus Assignments"