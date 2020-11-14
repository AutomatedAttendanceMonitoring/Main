from django.db import models
import uuid


# Create your models here.
class YearOfEducation(models.Model):
    number = models.CharField(primary_key=True, max_length=10)


class Student(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    FName = models.CharField(max_length=50)
    LName = models.CharField(max_length=50)
    year_of_education = models.ForeignKey(YearOfEducation, models.DO_NOTHING)
    statistics = models.DecimalField(decimal_places=3, default=None, max_digits=4)


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    year = models.ForeignKey(YearOfEducation, models.DO_NOTHING)


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    kind = models.CharField(max_length=10)
    subject = models.ForeignKey(Subject, models.DO_NOTHING)
    statistics = models.DecimalField(decimal_places=3, default=None, max_digits=4)


class IsTaughtBy(models.Model):
    subject = models.ForeignKey(Subject, models.DO_NOTHING)
    instructor = models.ForeignKey(Lesson, models.DO_NOTHING)


class IsPresent(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING)
    lesson = models.ForeignKey(Lesson, models.DO_NOTHING)


class AttendanceLink(models.Model):
    link_parameter = models.CharField(max_length=256, primary_key=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    lesson = models.ForeignKey(Lesson, models.DO_NOTHING)
