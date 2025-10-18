from django.urls import path
from .views import DashboardView
from .driver_views import mark_attendance, update_location, report_issue, view_full_route
from .parent_views import track_bus, notification_settings, child_schedule, attendance_history

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    # Driver URLs
    path('driver/attendance/', mark_attendance, name='driver_attendance'),
    path('driver/location/', update_location, name='update_location'),
    path('driver/issue/', report_issue, name='report_issue'),
    path('driver/route/', view_full_route, name='view_full_route'),
    # Parent URLs
    path('parent/track-bus/', track_bus, name='track_bus'),
    path('parent/notifications/', notification_settings, name='notification_settings'),
    path('parent/schedule/', child_schedule, name='child_schedule'),
    path('parent/attendance/', attendance_history, name='attendance_history'),
    path('parent/attendance/<int:student_id>/', attendance_history, name='attendance_history_detail'),
]