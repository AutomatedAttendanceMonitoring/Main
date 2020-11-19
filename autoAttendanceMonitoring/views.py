from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from autoAttendanceMonitoring.models import Student, IsPresent
from utils.db_commands import mark_student_attendance
from utils.link_sender import send_link_to
from utils.services.export_to_csv import CsvService


def index(request):
    if request.method == "POST":
        return HttpResponseRedirect("/send_links/aca9956a-4e37-400c-9a0b-b83290ffabca")
    return render(request, 'main/main-page.html')


def log_in(request):
    return render(request, 'main/log-in.html')


def manual_check(request):
    template = loader.get_template('main/manual-check.html')
    students = Student.objects.order_by('-email')
    context = {
        'students': students,
    }
    if request.method == "POST":
        print(request.POST)
        a = Student(
            email=request.POST['student-email'],
            FName=request.POST['student-name'],
            LName=request.POST['student-lname'],
            year_of_education_id=request.POST['student-year']
        )
        a.save()
        return HttpResponseRedirect("/manual-check")
    return HttpResponse(template.render(context, request))


def mark_student(request, link_parameter):
    try:
        mark_student_attendance(f"http://127.0.0.1:8000/markattendance/{link_parameter}")
        return HttpResponse("200 OK")
    except:
        return HttpResponse("403 error")


def send_links(request, lesson_id):
    try:
        students = Student.objects.all()
        for student in students:
            send_link_to(student, lesson_id)
        return HttpResponse("200 OK")
    except Exception:
        return HttpResponse("500 server error")


def export_to_csv(request, path):
    CsvService.export_from_db(IsPresent, path)
    return HttpResponse("200 OK")
