# Generated by Django 4.2.1 on 2023-07-27 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0033_alter_assignment_title_alter_certificate_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='content',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
