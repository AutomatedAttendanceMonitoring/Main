# Generated by Django 3.1.2 on 2020-11-22 09:37

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YearOfEducation',
            fields=[
                ('number', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ZoomAuth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_token', models.CharField(default='', max_length=700)),
                ('refresh_token', models.CharField(default='', max_length=700)),
                ('expires_at', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc), verbose_name='expiration time')),
                ('client_id', models.CharField(max_length=25)),
                ('client_secret', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ZoomParticipants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_id', models.CharField(max_length=12)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autoAttendanceMonitoring.yearofeducation')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('email', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('FName', models.CharField(max_length=50)),
                ('LName', models.CharField(max_length=50)),
                ('statistics', models.IntegerField(default=None)),
                ('year_of_education', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autoAttendanceMonitoring.yearofeducation')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('kind', models.CharField(max_length=10)),
                ('statistics', models.IntegerField(default=None)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autoAttendanceMonitoring.subject')),
            ],
        ),
        migrations.CreateModel(
            name='IsTaughtBy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autoAttendanceMonitoring.lesson')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autoAttendanceMonitoring.subject')),
            ],
        ),
        migrations.CreateModel(
            name='IsPresent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autoAttendanceMonitoring.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autoAttendanceMonitoring.student')),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceLink',
            fields=[
                ('link_parameter', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autoAttendanceMonitoring.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autoAttendanceMonitoring.student')),
            ],
        ),
    ]
