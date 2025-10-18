from django.db import models

class Route(models.Model):
    route_name = models.CharField(max_length=100)
    bus = models.ForeignKey('buses.Bus', on_delete=models.CASCADE)
    start_time = models.TimeField()
    estimated_duration = models.DurationField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.route_name} - Bus {self.bus.bus_number}"
    
    class Meta:
        verbose_name_plural = "Routes"

class PickupPoint(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    estimated_pickup_time = models.TimeField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Pickup Points"

class RoutePoint(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE)
    sequence_order = models.IntegerField()
    
    def __str__(self):
        return f"{self.route.route_name} - Stop {self.sequence_order}: {self.pickup_point.name}"
    
    class Meta:
        ordering = ['sequence_order']
        verbose_name_plural = "Route Points"