from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from buses.models import Bus
from students.models import Student, StudentBusAssignment
from routes.models import Route, RoutePoint
from tracking.models import BusLocation, StudentAttendance
from bus_notifications.models import Notification
from django.utils import timezone
from datetime import date
from django.contrib.auth import logout  # ← ADD THIS
from django.shortcuts import redirect  # 

def custom_logout(request):
    """Custom logout view that accepts GET requests and redirects to home"""
    logout(request)
    return redirect('/')  # Redirect to home page after logout

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/main_dashboard.html'
    login_url = '/accounts/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Common stats for all users
        context['total_buses'] = Bus.objects.count()
        context['active_buses'] = Bus.objects.filter(is_active=True).count()
        context['total_students'] = Student.objects.count()
        context['active_routes'] = Route.objects.filter(is_active=True).count()
        
        # User-specific data
        context['user_type'] = user.user_type
        
        if user.user_type == 'parent':
            # Get parent's children with their bus assignments
            children = Student.objects.filter(parent=user)
            context['my_children'] = children
            
            # Get bus assignments for these children
            child_bus_data = []
            for child in children:
                assignment = StudentBusAssignment.objects.filter(
                    student=child, 
                    is_active=True
                ).first()
                if assignment:
                    child_bus_data.append({
                        'child': child,
                        'bus': assignment.bus,
                        'route': Route.objects.filter(bus=assignment.bus, is_active=True).first()
                    })
            
            context['child_bus_data'] = child_bus_data
            
            # Get recent notifications
            context['recent_notifications'] = Notification.objects.filter(
                recipients=user
            ).order_by('-created_at')[:5]
            
            # Get today's attendance for children
            context['today_attendance'] = StudentAttendance.objects.filter(
                student__in=children,
                date=date.today()
            )

        elif user.user_type == 'driver':
            # Driver-specific data
            # Get driver's assigned bus
            driver_assignments = user.driverassignment_set.filter(is_active=True)
            if driver_assignments.exists():
                assigned_bus = driver_assignments.first().bus
                context['assigned_bus'] = assigned_bus
                context['assigned_route'] = Route.objects.filter(bus=assigned_bus, is_active=True).first()
                
                # Get students assigned to this bus
                student_assignments = StudentBusAssignment.objects.filter(
                    bus=assigned_bus, 
                    is_active=True
                )
                context['assigned_students'] = [assignment.student for assignment in student_assignments]
                
                # Get today's attendance for assigned students
                context['today_attendance'] = StudentAttendance.objects.filter(
                    student__in=context['assigned_students'],
                    date=date.today()
                )
                
                # Get route points if route exists
                if context['assigned_route']:
                    context['route_points'] = RoutePoint.objects.filter(
                        route=context['assigned_route']
                    ).order_by('sequence_order')
            
        elif user.user_type in ['admin', 'school_staff']:
            # Admin-specific data
            context['recent_locations'] = BusLocation.objects.all().order_by('-timestamp')[:10]
            context['today_attendance'] = StudentAttendance.objects.filter(date=date.today())
            context['pending_notifications'] = Notification.objects.filter(is_sent=False)
        
        return context