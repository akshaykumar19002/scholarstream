from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

import html

from .models import Chat, Message
from course.models import Course
from .forms import EmailForm
from notifications.utils import create_notification
from user.models import BlockedUsers

@login_required
def chat_room(request, chat_id, course_id):
    course = get_object_or_404(Course, pk=course_id)
    messages = Message.objects.filter(chat_id=chat_id).order_by('timestamp')
    chat = Chat.objects.get(pk=chat_id)
    return render(request, 'chat/chat.html', {'chat_id': chat_id, 'course': course, 'messages': messages, 'chat': chat})


@login_required
def create_chat_room(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    instructor = get_user_model().objects.filter(courses = course, user_type='I').first()
    Chat.objects.create(student=request.user, instructor=instructor)
    chat_room = Chat.objects.filter(student=request.user, instructor=instructor).first()
    create_notification(instructor, 'chat', f'You have received a new chat request from {request.user.first_name}.', reverse('chat:chat_room', args=[chat_room.id, course.id]))
    return redirect('chat:chat_room', chat_room.id, course.id)


@login_required
def contact_options(request, course_id, student_id=None):
    course = get_object_or_404(Course, pk=course_id)
    if student_id:
        student = get_user_model().objects.get(pk=student_id)
        last_chat = Chat.objects.filter(student_id=student, instructor=request.user).last()
        return render(request, 'chat/contact_options.html', {'course': course, 'last_chat': last_chat, 'is_instructor': True, 'student_id': student_id})
    else:
        last_chat = Chat.objects.filter(student=request.user, instructor__courses=course).last()
        return render(request, 'chat/contact_options.html', {'course': course, 'last_chat': last_chat, 'is_instructor': False})


@login_required
def contact_email(request, course_id, student_id=None):
    course = get_object_or_404(Course, pk=course_id)
    instructor = get_user_model().objects.filter(courses = course, user_type='I').first()
    is_blocked = BlockedUsers.objects.filter(student=request.user, instructor=instructor, course=course).exists()

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.sender = request.user
            if student_id:
                email.recipient = get_user_model().objects.get(pk=student_id)
            else:
                email.recipient = get_user_model().objects.filter(courses = course, user_type='I').first()
            email.save()
            email.content = html.unescape(email.content)
            email.content = f"<p><strong>Email sent from {email.sender.first_name}</strong></p><hr><br><br><p>{email.content}</p>"
            email.recipient.email_user(email.subject, email.content, html_message=email.content)
            create_notification(email.recipient, 'email', f'You have received an email from {email.sender.first_name}.')
            if student_id:
                return redirect('chat:contact_options_for_student', course_id, student_id)
            return redirect('chat:contact_options', course_id)
    emailForm = EmailForm()
    return render(request, 'chat/contact_email.html', {'form': emailForm, 'course': course, 'is_blocked': is_blocked})


@login_required
def block_student(request, course_id, student_id):
    if request.user.user_type == 'S':
        return redirect('forbidden')
    student = get_object_or_404(get_user_model(), pk=student_id)
    course = get_object_or_404(Course, pk=course_id)
    BlockedUsers.objects.get_or_create(student=student, course=course, instructor=request.user)
    return redirect('course:list_students', course_id)
    
@login_required
def unblock_student(request, course_id, student_id):
    if request.user.user_type == 'S':
        return redirect('forbidden')
    student = get_object_or_404(get_user_model(), pk=student_id)
    course = get_object_or_404(Course, pk=course_id)
    get_object_or_404(BlockedUsers, student=student, course=course, instructor=request.user).delete()
    return redirect('course:list_students', course_id)
 
