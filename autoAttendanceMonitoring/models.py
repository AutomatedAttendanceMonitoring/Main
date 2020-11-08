from django.db import models


# Create your models here.
class Student(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)


class AttendanceLink(models.Model):
    link_parameter = models.CharField(max_length=50, primary_key=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    lesson = models.ForeignKey(Lesson, models.DO_NOTHING)
