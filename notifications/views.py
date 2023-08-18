from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.core.paginator import Paginator
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model

from .models import Notification, Announcement
from .forms import AnnouncementForm
from course.models import Course
from .utils import send_notifications_for_all_students


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

def create_announcement(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if get_user_model().objects.filter(courses = course, pk=request.user.id, user_type='I').count() == 0:
        return redirect('forbidden')
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.instructor = request.user
            announcement.course = course
            announcement.save()
            send_notifications_for_all_students(course, 'announcement', 'New announcement `' + announcement.title + '`in ' + course.name, reverse('notifications:view_announcement', args=[course_id, announcement.id]))
            return redirect('notifications:view_all_announcements', course_id)
    else:
        form = AnnouncementForm()
    return render(request, 'notifications/announcements/add.html', {'form': form, 'course': course})


def view_all_announcements(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    announcements = Announcement.objects.filter(course=course).order_by('-created_at')
    
    paginator = Paginator(announcements, 8)
    page = request.GET.get('page')
    announcements = paginator.get_page(page)
    
    for announcement in announcements:
        announcement.content = strip_tags(announcement.content)
        announcement.content = announcement.content[:100] + '...'
    
    return render(request, 'notifications/announcements/view_all.html', {'announcements': announcements, 'course': course,})


def view_announcement(request, course_id, announcement_id):
    course = get_object_or_404(Course, pk=course_id)
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    return render(request, 'notifications/announcements/view.html', {'announcement': announcement, 'course': course})


def edit_announcement(request, course_id, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    course = get_object_or_404(Course, pk=course_id)
    if request.user != announcement.instructor:
        return redirect('forbidden')
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            send_notifications_for_all_students(course, 'announcement', 'Announcement `' + announcement.title + '`updated in ' + course.name, reverse('notifications:view_announcement', args=[course_id, announcement.id]))
            return redirect('notifications:view_announcement', announcement.course.id, announcement.id)
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'notifications/announcements/edit.html', {'form': form, 'announcement': announcement, 'course': course})

def delete_announcement(request, course_id, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    if request.user != announcement.instructor:
        return redirect('forbidden')
    announcement.delete()
    return redirect('notifications:view_all_announcements', course_id)
