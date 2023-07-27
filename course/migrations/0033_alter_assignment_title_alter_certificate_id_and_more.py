# Generated by Django 4.2.1 on 2023-07-27 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0032_alter_certificate_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='id',
            field=models.CharField(default='9b995fc2e4c34905a69e2667137e71be', editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='content',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='title',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='othergrade',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]