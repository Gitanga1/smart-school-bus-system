from django.db import models
from accounts.models import User

class Bus(models.Model):
    bus_number = models.CharField(max_length=10, unique=True)
    license_plate = models.CharField(max_length=15, unique=True)
    capacity = models.IntegerField()
    current_driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'user_type': 'driver'})
    gps_device_id = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Bus {self.bus_number}"
    class Meta:
        verbose_name_plural = "Buses"

class DriverAssignment(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'driver'})
    assigned_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.driver.username} -> Bus {self.bus.bus_number}"