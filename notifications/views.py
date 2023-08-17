from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .models import Notification

def list_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    
    paginator = Paginator(notifications, 8)
    page = request.GET.get('page')
    notifications = paginator.get_page(page)
    
    for notification in notifications:
        notification.is_read = True
        notification.save()
    
    return render(request, 'notifications/list_notifications.html', {'notifications': notifications, 'is_all': False})

def view_all_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(notifications, 8)
    page = request.GET.get('page')
    notifications = paginator.get_page(page)
    return render(request, 'notifications/list_notifications.html', {'notifications': notifications, 'is_all': True})