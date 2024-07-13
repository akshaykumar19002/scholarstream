# Generated by Django 4.2.1 on 2023-08-17 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0036_alter_course_thumbnail'),
        ('notifications', '0004_notification_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='content_type',
            field=models.CharField(choices=[('email', 'Email'), ('announcement', 'Announcement'), ('grade', 'Grade'), ('chat', 'Chat'), ('course_purchase', 'Course Purchase'), ('course_content', 'Course Content'), ('assignment_grade', 'Assignment Graded'), ('extra_grades', 'Extra Grade'), ('certificate', 'Certificate'), ('registration', 'Registration'), ('password_changed', 'Password Changed'), ('username_changed', 'Username Changed')], max_length=20),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='course.course')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]