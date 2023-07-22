# Generated by Django 4.2.1 on 2023-07-21 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_usermodel_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_type',
            field=models.CharField(choices=[('S', 'Student'), ('I', 'Instructor')], default='S', max_length=2),
        ),
    ]
