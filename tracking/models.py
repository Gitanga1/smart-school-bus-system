from django.db import models
from django.utils import timezone

class BusLocation(models.Model):
    bus = models.ForeignKey('buses.Bus', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # km/h
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Bus {self.bus.bus_number} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Bus Locations"

class StudentAttendance(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    bus = models.ForeignKey('buses.Bus', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    boarded_time = models.DateTimeField(null=True, blank=True)
    exited_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('pending', 'Pending')
    ], default='pending')
    
    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"
    
    class Meta:
        verbose_name_plural = "Student Attendance"
        unique_together = ['student', 'date']