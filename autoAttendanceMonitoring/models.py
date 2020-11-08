from django.db import models


# Create your models here.
class Student(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)


class AttendanceLink(models.Model):
    link_parameter = models.CharField(max_length=50, primary_key=True)
    student_email = models.CharField(max_length=256)
