from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date
from tracking.models import StudentAttendance, BusLocation
from buses.models import Bus
from students.models import Student
from bus_notifications.models import Notification
from django.contrib import messages
import random

@login_required
def mark_attendance(request):
    """Driver marks attendance for students on their bus"""
    if request.user.user_type != 'driver':
        return redirect('home')
    
    # Get driver's assigned bus
    driver_assignments = request.user.driverassignment_set.filter(is_active=True)
    if not driver_assignments.exists():
        messages.error(request, "No bus assigned to you.")
        return redirect('home')
    
    assigned_bus = driver_assignments.first().bus
    assigned_students = Student.objects.filter(
        studentbusassignment__bus=assigned_bus,
        studentbusassignment__is_active=True
    )
    
    if request.method == 'POST':
        # Process attendance form
        for student in assigned_students:
            status = request.POST.get(f'status_{student.id}', 'absent')
            attendance, created = StudentAttendance.objects.get_or_create(
                student=student,
                bus=assigned_bus,
                date=date.today(),
                defaults={'status': 'pending'}
            )
            
            if status == 'present':
                attendance.status = 'present'
                attendance.boarded_time = timezone.now()
            elif status == 'absent':
                attendance.status = 'absent'
            
            attendance.save()
        
        messages.success(request, "Attendance marked successfully!")
        return redirect('driver_attendance')
    
    # Get today's existing attendance
    today_attendance = StudentAttendance.objects.filter(
        student__in=assigned_students,
        date=date.today()
    )
    
    context = {
        'assigned_bus': assigned_bus,
        'assigned_students': assigned_students,
        'today_attendance': today_attendance,
    }
    return render(request, 'dashboard/driver_attendance.html', context)

@login_required
def update_location(request):
    """Driver updates their current GPS location"""
    if request.user.user_type != 'driver':
        return redirect('home')
    
    # Get driver's assigned bus
    driver_assignments = request.user.driverassignment_set.filter(is_active=True)
    if not driver_assignments.exists():
        messages.error(request, "No bus assigned to you.")
        return redirect('home')
    
    assigned_bus = driver_assignments.first().bus
    
    if request.method == 'POST':
        # Simulate GPS coordinates (in real app, get from device)
        latitude = request.POST.get('latitude', 40.7128 + random.uniform(-0.01, 0.01))
        longitude = request.POST.get('longitude', -74.0060 + random.uniform(-0.01, 0.01))
        speed = random.randint(20, 60)  # Simulated speed
        
        # Create location record
        BusLocation.objects.create(
            bus=assigned_bus,
            latitude=latitude,
            longitude=longitude,
            speed=speed
        )
        
        messages.success(request, f"Location updated! Speed: {speed} km/h")
        return redirect('update_location')
    
    # Get recent locations for this bus
    recent_locations = BusLocation.objects.filter(bus=assigned_bus).order_by('-timestamp')[:5]
    
    context = {
        'assigned_bus': assigned_bus,
        'recent_locations': recent_locations,
    }
    return render(request, 'dashboard/driver_location.html', context)

@login_required
def report_issue(request):
    """Driver reports issues or emergencies"""
    if request.user.user_type != 'driver':
        return redirect('home')
    
    if request.method == 'POST':
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')
        urgency = request.POST.get('urgency', 'medium')
        
        # Create notification for admins
        Notification.objects.create(
            notification_type='emergency',
            title=f"Driver Issue: {issue_type}",
            message=f"Driver {request.user.username} reports: {description}",
            scheduled_for=timezone.now()
        )
        
        messages.warning(request, f"Issue reported! Admin has been notified.")
        return redirect('report_issue')
    
    return render(request, 'dashboard/driver_issue.html')

@login_required
def view_full_route(request):
    """Driver views complete route details"""
    if request.user.user_type != 'driver':
        return redirect('home')
    
    # Get driver's assigned bus and route
    driver_assignments = request.user.driverassignment_set.filter(is_active=True)
    if not driver_assignments.exists():
        messages.error(request, "No bus assigned to you.")
        return redirect('home')
    
    assigned_bus = driver_assignments.first().bus
    assigned_route = assigned_bus.route_set.filter(is_active=True).first()
    
    if assigned_route:
        route_points = assigned_route.routepoint_set.all().order_by('sequence_order')
    else:
        route_points = []
        messages.info(request, "No active route assigned to your bus.")
    
    context = {
        'assigned_bus': assigned_bus,
        'assigned_route': assigned_route,
        'route_points': route_points,
    }
    return render(request, 'dashboard/driver_route.html', context)