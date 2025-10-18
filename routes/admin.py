from django.contrib import admin
from .models import Route, PickupPoint, RoutePoint

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('route_name', 'bus', 'start_time', 'estimated_duration', 'is_active')
    list_filter = ('is_active', 'bus')
    search_fields = ('route_name',)

@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'estimated_pickup_time')
    search_fields = ('name', 'address')

@admin.register(RoutePoint)
class RoutePointAdmin(admin.ModelAdmin):
    list_display = ('route', 'pickup_point', 'sequence_order')
    list_filter = ('route',)
    ordering = ('route', 'sequence_order')