# Generated by Django 4.2.1 on 2023-06-11 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='is_paid',
        ),
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
