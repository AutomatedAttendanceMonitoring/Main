from django.conf.urls import url
from django.urls import path
from autoAttendanceMonitoring import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^markattendance/', views.mark_student, name='mark_student')
]
