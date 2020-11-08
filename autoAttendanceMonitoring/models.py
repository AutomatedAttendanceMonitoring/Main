from django.db import models
import uuid


# Create your models here.
class year_of_education(model.Model):
    number = models.CharField(primary_key=True, max_length=10)

class students(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    FName = models.CharField(max_length=50)
    LName = models.CharField(max_length=50)
    year_of_education = models.ForeignKey('year_of_education')
    

class subjects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    year = models.ForeignKey('year_of_education')
    

class lessons(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    kind = models.CharField(max_length=10)
    subject = models.ForeignKey('subjects')
    
class is_taught_by(models.Model):
    subject = models.ForeignKey('subjects')
    instructor = models.ForeignKey('lessons')
    
class is_present(models.Model):
    student = models.ForeignKey('students')
    lesson = models.ForeignKey('lessons')
    
class AttendanceLink(models.Model):
    link_parameter = models.CharField(max_length=50, primary_key=True)
    student_email = models.CharField(max_length=256)