from django.urls import path
from autoAttendanceMonitoring import views

urlpatterns = [
    path('log-in/', views.log_in, name="Login page"),
    path('markattendance/<str:link_parameter>', views.mark_student, name='mark_student'),
    path('send_links/<str:lesson_id>', views.send_links, name='links_sender'),
    path('manual-check/', views.manual_check, name='manual-check'),
    path('', views.index, name="Main page"),
    path('zoom/send-messages', views.send_messages, name='zoom-send-messages'),
    path('zoom/set-credentials', views.set_credentials, name='zoom-set-credentials'),
    # path('zoom/token-callback', views.token_callback, name='zoom-token-callback'),
]
