# Generated by Django 4.2.1 on 2023-07-01 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_assignmentsubmission_grader'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='quizattempt',
            unique_together=set(),
        ),
    ]
