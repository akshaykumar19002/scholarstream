# Generated by Django 4.2.1 on 2023-08-18 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='instructor_online',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chat',
            name='student_online',
            field=models.BooleanField(default=False),
        ),
    ]