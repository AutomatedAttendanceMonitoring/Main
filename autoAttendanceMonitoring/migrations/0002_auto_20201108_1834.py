# Generated by Django 3.1.2 on 2020-11-08 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoAttendanceMonitoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancelink',
            name='link_parameter',
            field=models.CharField(max_length=256, primary_key=True, serialize=False),
        ),
    ]