from django.http import HttpResponse
from django.shortcuts import render

from utils.db_commands import get_student_by_link_parameter, mark_student_attendance


def index(request):
    return render(request, 'main/main-page.html')


def mark_student(request, link_parameter):
    try:
        mark_student_attendance(link_parameter)
        return HttpResponse("200 OK")
    except:
        return HttpResponse("403 error")


def send_links(request):
    # students =