# Generated by Django 4.2.1 on 2023-08-16 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_rename_content_notification_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]