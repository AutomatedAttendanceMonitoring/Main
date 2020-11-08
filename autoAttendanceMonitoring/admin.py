from django.contrib import admin
from autoAttendanceMonitoring.models import Student, AttendanceLink, YearOfEducation, IsPresent, IsTaughtBy, Lesson, \
    Subject

# Register your models here.
admin.site.register(YearOfEducation)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(IsTaughtBy)
admin.site.register(IsPresent)
admin.site.register(Student)
admin.site.register(AttendanceLink)
