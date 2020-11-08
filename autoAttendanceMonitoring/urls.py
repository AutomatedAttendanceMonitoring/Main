from django.conf.urls import url
from django.urls import path
from autoAttendanceMonitoring import views

urlpatterns = [
    path(r'markattendance/<str:link_parameter>', views.mark_student, name='mark_student')
]
