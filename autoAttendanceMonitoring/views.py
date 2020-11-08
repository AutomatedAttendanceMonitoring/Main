from django.http import HttpResponse
from django.shortcuts import render

from autoAttendanceMonitoring.models import Student
from utils.db_commands import get_student_by_link_parameter, mark_student_attendance
from utils.link_sender import send_link_to


def index(request):
    return render(request, 'main/main-page.html')


def mark_student(request, link_parameter):
    try:
        mark_student_attendance(link_parameter)
        return HttpResponse("200 OK")
    except:
        return HttpResponse("403 error")


def send_links(request, lesson_id):
    try:
        students = Student.objects.all()
        for student in students:
            send_link_to(student, lesson_id)
        return HttpResponse("200 OK")
    except:
        return HttpResponse("500 server error")