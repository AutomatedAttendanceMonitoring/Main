from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from autoAttendanceMonitoring.models import Student
from utils.db_commands import get_student_by_link_parameter, mark_student_attendance
from utils.link_sender import send_link_to


def index(request):
    return render(request, 'main/main-page.html')

def manual_check(request):
    template = loader.get_template('main/manual-check.html')
    students = Student.objects.order_by('-id')
    context = {
        'students' : students,
    }
    if request.method == "POST":
        print(request.POST)
        a = Student(id=int(students[0].id)+1, name=request.POST['student-name'])
        a.save()
        return HttpResponseRedirect("/manual-check")
    return HttpResponse(template.render(context,request))


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