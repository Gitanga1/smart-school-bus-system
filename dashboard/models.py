from django.db import models
from django.utils import timezone

class SystemStats(models.Model):
    total_buses = models.IntegerField(default=0)
    active_buses = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    active_routes = models.IntegerField(default=0)
    students_transported_today = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"System Stats - {self.last_updated}"
    
    class Meta:
        verbose_name_plural = "System Statistics"