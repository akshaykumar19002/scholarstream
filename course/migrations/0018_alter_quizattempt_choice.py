# Generated by Django 4.2.1 on 2023-07-01 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0017_remove_quizattempt_is_complete_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizattempt',
            name='choice',
            field=models.CharField(max_length=100),
        ),
    ]
