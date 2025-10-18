from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()  # notifications

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('delay', 'Bus Delay'),
        ('arrival', 'Bus Arrival'),
        ('emergency', 'Emergency'),
        ('route_change', 'Route Change'),
        ('maintenance', 'Maintenance'),
        ('weather', 'Weather Alert'),
        ('info', 'Information'),  # for notifications
    )
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)  
    recipients = models.ManyToManyField(User, blank=True, related_name='received_notifications')  
    bus = models.ForeignKey('buses.Bus', on_delete=models.SET_NULL, null=True, blank=True)  
    created_at = models.DateTimeField(default=timezone.now)
    is_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)  #  (for tracking read status)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.notification_type}: {self.title}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Notifications"

class NotificationTemplate(models.Model):
    name = models.CharField(max_length=100)
    notification_type = models.CharField(max_length=20, choices=Notification.NOTIFICATION_TYPES)
    subject_template = models.CharField(max_length=200)
    message_template = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Notification Templates"