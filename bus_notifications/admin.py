from django.contrib import admin
from .models import Notification, NotificationTemplate

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'created_at', 'is_sent', 'scheduled_for')
    list_filter = ('notification_type', 'is_sent', 'created_at')
    filter_horizontal = ('recipients',)
    readonly_fields = ('created_at',)
    search_fields = ('title', 'message')

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'notification_type', 'subject_template')
    list_filter = ('notification_type',)
    search_fields = ('name', 'subject_template')