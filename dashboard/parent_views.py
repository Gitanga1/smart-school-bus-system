from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from students.models import Student, StudentBusAssignment
from buses.models import Bus
from routes.models import Route, RoutePoint
from tracking.models import BusLocation, StudentAttendance
from bus_notifications.models import Notification
from django.contrib import messages
import random

@login_required
def track_bus(request):
    """Parent views real-time bus location for their children"""
    if request.user.user_type != 'parent':
        return redirect('home')
    
    # Get parent's children and their bus assignments
    children = Student.objects.filter(parent=request.user)
    child_bus_data = []
    
    for child in children:
        assignment = StudentBusAssignment.objects.filter(
            student=child, 
            is_active=True
        ).first()
        if assignment:
            # Get latest bus location
            latest_location = BusLocation.objects.filter(
                bus=assignment.bus
            ).order_by('-timestamp').first()
            
            # Get route information
            route = Route.objects.filter(
                bus=assignment.bus, 
                is_active=True
            ).first()
            
            child_bus_data.append({
                'child': child,
                'bus': assignment.bus,
                'route': route,
                'latest_location': latest_location,
                'estimated_arrival': calculate_estimated_arrival(latest_location, route) if latest_location and route else "Calculating..."
            })
    
    context = {
        'child_bus_data': child_bus_data,
        'map_center': {'lat': 40.7128, 'lng': -74.0060},  # Default center
    }
    return render(request, 'dashboard/parent_track_bus.html', context)

@login_required
def notification_settings(request):
    """Parent manages notification preferences"""
    if request.user.user_type != 'parent':
        return redirect('home')
    
    if request.method == 'POST':
        # In a real app, save notification preferences to user profile
        messages.success(request, "Notification settings updated successfully!")
        return redirect('notification_settings')
    
    # Get recent notifications for this parent
    recent_notifications = Notification.objects.filter(
        recipients=request.user
    ).order_by('-created_at')[:20]
    
    context = {
        'recent_notifications': recent_notifications,
    }
    return render(request, 'dashboard/parent_notifications.html', context)

@login_required
def child_schedule(request):
    """Parent views detailed schedule for their children"""
    if request.user.user_type != 'parent':
        return redirect('home')
    
    children = Student.objects.filter(parent=request.user)
    schedule_data = []
    
    for child in children:
        assignment = StudentBusAssignment.objects.filter(
            student=child, 
            is_active=True
        ).first()
        
        if assignment and assignment.bus:
            route = Route.objects.filter(
                bus=assignment.bus, 
                is_active=True
            ).first()
            
            if route:
                # Generate weekly schedule
                schedule_data.append({
                    'child': child,
                    'bus': assignment.bus,
                    'route': route,
                    'pickup_time': route.start_time,
                    'dropoff_time': calculate_dropoff_time(route.start_time, route.estimated_duration),
                    'stops': RoutePoint.objects.filter(route=route).order_by('sequence_order')
                })
    
    context = {
        'schedule_data': schedule_data,
        'today': datetime.now().strftime("%A, %B %d, %Y")
    }
    return render(request, 'dashboard/parent_schedule.html', context)

@login_required
def attendance_history(request, student_id=None):
    """Parent views attendance history for their children"""
    if request.user.user_type != 'parent':
        return redirect('home')
    
    children = Student.objects.filter(parent=request.user)
    selected_child = None
    attendance_history = []
    
    if student_id:
        selected_child = get_object_or_404(Student, id=student_id, parent=request.user)
        attendance_history = StudentAttendance.objects.filter(
            student=selected_child
        ).order_by('-date')[:30]  # Last 30 days
    
    context = {
        'children': children,
        'selected_child': selected_child,
        'attendance_history': attendance_history,
    }
    return render(request, 'dashboard/parent_attendance.html', context)

# Helper functions
def calculate_estimated_arrival(location, route):
    """Calculate estimated arrival time (simplified)"""
    if location and route:
        # Simple simulation - in real app, use actual routing
        base_time = route.start_time
        arrival_time = datetime.combine(datetime.today(), base_time) + timedelta(minutes=random.randint(5, 15))
        return arrival_time.strftime("%I:%M %p")
    return "Not available"

def calculate_dropoff_time(start_time, duration):
    """Calculate dropoff time based on route start and duration"""
    if start_time and duration:
        # Convert time to datetime for calculation
        start_dt = datetime.combine(datetime.today(), start_time)
        dropoff_dt = start_dt + duration
        return dropoff_dt.time().strftime("%I:%M %p")
    return "Not available"