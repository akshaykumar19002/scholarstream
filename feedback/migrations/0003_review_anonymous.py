# Generated by Django 4.2.1 on 2023-07-07 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_rename_text_review_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='anonymous',
            field=models.BooleanField(default=False),
        ),
    ]
