from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, redirect
from django.urls import reverse
import requests
import re

from .models import ZoomAuth, Lesson, Subject
from django.template import loader

from autoAttendanceMonitoring.models import Student, IsPresent
from utils.db_commands import mark_student_attendance
from utils.link_sender import send_link_to
from utils.services.export_to_csv import CsvService


def index(request):
    if request.method == "POST":
        return HttpResponseRedirect("/send_links/aca9956a-4e37-400c-9a0b-b83290ffabca")
    return render(request, 'main/main-page.html')


# region Zoom API
# warning: needs to be protected
# TODO: switch to POST methods
def send_messages(request):
    email_regex = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")
    auth = ZoomAuth.objects.first()
    if auth is None or auth.token is None:
        return HttpResponse(f"Error: Zoom token is not present. Go to https://{request.get_host()}{reverse('zoom-set-credentials')} "
                            "passing your client_id and client_secret values as query parameters.\n")

    users: list[str] = list(filter(email_regex.fullmatch, request.GET.get("users", "").split(",")))
    message: str = request.GET.get("message")
    if len(users) == 0:
        return HttpResponse("Error: No valid emails found.")
    elif message is None or message == "":
        return HttpResponse("Error: Message is empty.")

    url = "https://api.zoom.us/v2/chat/users/me/messages"
    result = ""
    for email in users:
        result += str(requests.post(url, data=f'{{"message": "{message}","to_contact":"{email}"}}', headers={
            'content-type': "application/json",
            'authorization': f"Bearer {auth.token}"
        }).json()) + "\n"
    return HttpResponse(f"<pre>{result}</pre>")


def set_credentials(request):
    client_id = request.GET.get("client_id")
    client_secret = request.GET.get("client_secret")
    if client_id is None or client_secret is None:
        return HttpResponse("Error: client_id and client_secret are required\n")
    else:
        try:
            ZoomAuth.objects.update_or_create(defaults={
                "client_id": client_id, "client_secret": client_secret
            })
        except MultipleObjectsReturned:
            return HttpResponse("Error: multiple token records, check DB manually\n")
        return redirect(f"https://zoom.us/oauth/authorize?response_type=code&client_id={client_id}&"
                        f"redirect_uri=https://{request.get_host()}{reverse('zoom-token-callback')}&"
                        f"state=https://{request.get_host()}{reverse('zoom-token-callback')}", permanent=True)


def token_callback(request):
    auth_code = request.GET.get("code")
    redirect_uri = request.GET.get("state")
    success: bool = ZoomAuth.objects.first().new_token(auth_code, redirect_uri)
    return HttpResponse("Obtained new tokens successfully\n" if success else "Error obtaining new tokens, yet client info was saved")
# endregion


def mark_read(request):
    pass


def log_in(request):
    return render(request, 'main/log-in.html')


def select_lesson(request):
    template = loader.get_template('main/select-lesson.html')
    lessons = Lesson.objects.all()
    subjects = Subject.objects.all()

    context = {
        'lessons': lessons,
        'subjects': subjects,
    }
    if request.method == 'POST':
        lesson = Lesson(
            subject=Subject.objects.get(pk=request.POST['lesson-subject']),
            # TODO извлечь время из html
            start_time=datetime.strptime(request.POST['date-start'], '%d/%m/%Y - %H:%M'),
            end_time=datetime.strptime(request.POST['date-end'], '%d/%m/%Y - %H:%M'),
            kind=request.POST['lesson-kind'],
        )
        lesson.save()
        return HttpResponseRedirect("/select-lesson")
    return HttpResponse(template.render(context, request))


def manual_check(request, lesson_id):
    template = loader.get_template('main/manual-check.html')
    lesson = Lesson.objects.get(pk=lesson_id)

    marked_students = IsPresent.objects.filter(lesson_id=lesson_id)
    students = Student.objects.filter(year_of_education=lesson.subject.year)
    context = {
        'students': students,
        'marked_students': marked_students,
    }
    if request.method == "POST":
        print(request.POST)
        student = Student.objects.get(pk=request.POST['student-to-mark'])
        present = IsPresent(
            student=student,
            lesson_id=lesson_id
        )
        present.save()
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

