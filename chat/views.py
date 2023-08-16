from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

import html

from .models import Chat, Message
from course.models import Course
from .forms import EmailForm

@login_required
def chat_room(request, chat_id, course_id):
    course = get_object_or_404(Course, pk=course_id)
    messages = Message.objects.filter(chat_id=chat_id).order_by('timestamp')
    return render(request, 'chat/chat.html', {'chat_id': chat_id, 'course': course, 'messages': messages})


@login_required
def create_chat_room(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    instructor = get_user_model().objects.filter(courses = course, user_type='I').first()
    Chat.objects.create(student=request.user, instructor=instructor)
    chat_room = Chat.objects.filter(student=request.user, instructor=instructor).first()
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
            if student_id:
                return redirect('chat:contact_options_for_student', course_id, student_id)
            return redirect('chat:contact_options', course_id)
    emailForm = EmailForm()
    return render(request, 'chat/contact_email.html', {'form': emailForm, 'course': course})
