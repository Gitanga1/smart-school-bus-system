from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from buses.models import Bus
from .models import Notification  

@login_required
def notification_list(request):               
    """Display all notifications for the current user"""
    notifications = Notification.objects.filter(recipients=request.user).order_by('-created_at')
    return render(request, 'bus_notifications/notification_list.html', {
        'notifications': notifications
    })

@login_required
def send_notification(request):
    if request.user.user_type not in ['admin', 'school_staff']:
        messages.error(request, "You don't have permission to send notifications.")
        return redirect('home')
    
    # Get users grouped by type
    user_groups = {
        'parent': User.objects.filter(user_type='parent'),
        'driver': User.objects.filter(user_type='driver'),
        'admin': User.objects.filter(user_type='admin'),
    }
    
    buses = Bus.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # Handle form submission
        title = request.POST.get('title')
        message = request.POST.get('message')
        notification_type = request.POST.get('notification_type')
        bus_id = request.POST.get('bus')
        recipient_ids = request.POST.getlist('recipients')
        
        if not title or not message or not notification_type or not recipient_ids:
            messages.error(request, "Please fill all required fields.")
        else:
            notification = Notification.objects.create(
                title=title,
                message=message,
                notification_type=notification_type,
                sender=request.user,
                bus_id=bus_id if bus_id else None
            )
            
            # recipients
            recipients = User.objects.filter(id__in=recipient_ids)
            notification.recipients.set(recipients)
            
            messages.success(request, f'Notification sent to {recipients.count()} recipients!')
            return redirect('notification_list')
    
    return render(request, 'bus_notifications/send_notification.html', {
        'user_groups': user_groups,
        'buses': buses
    })

@login_required
def mark_as_read(request, notification_id):  
    """Mark a notification as read"""
    notification = Notification.objects.get(id=notification_id)
    if request.user in notification.recipients.all():
        notification.is_read = True
        notification.save()
        messages.success(request, "Notification marked as read.")
    else:
        messages.error(request, "You don't have permission to mark this notification as read.")
    
    return redirect('notification_list')