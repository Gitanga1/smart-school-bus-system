from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_notification, name='send_notification'),
    path('', views.notification_list, name='notification_list'),
    path('read/<int:notification_id>/', views.mark_as_read, name='mark_notification_read'),
]