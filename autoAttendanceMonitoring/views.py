from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import requests
import re

from .models import ZoomAuth
from django.template import loader

from autoAttendanceMonitoring.models import Student
from utils.db_commands import get_student_by_link_parameter, mark_student_attendance
from utils.link_sender import send_link_to


def index(request):
    return render(request, 'main/main-page.html')


# region Zoom API
def send_messages(request):
    # warning: needs to be protected
    email_regex = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")
    zoom_token = ZoomAuth.objects.first().token
    if zoom_token is None:
        return HttpResponse(f"Error: Zoom token is not present. Go to https://{request.get_host()}{reverse('zoom-set-credentials')} "
                            "passing your client_id and client_secret values as query parameters.")

    users: list[str] = list(filter(email_regex.fullmatch, request.GET.get("users", "").split(",")))
    message: str = request.GET.get("message")
    if len(users) == 0:
        return HttpResponse("Error: No valid emails found.")
    elif message is None or message == "":
        return HttpResponse("Error: Message is empty.")

    url = "https://api.zoom.us/v2/chat/users/me/messages"
    for email in users:
        print(requests.post(url, data=f'{"message": "{message}","to_contact":"{email}"}', headers={
            'content-type': "application/json",
            'authorization': f"Bearer {zoom_token}"
        }).json())
    return HttpResponse("ok")


def set_credentials(request):
    client_id = request.GET.get("client_id")
    client_secret = request.GET.get("client_secret")
    if client_id is None or client_secret is None:
        return HttpResponse("Error: client_id and client_secret are required")
    else:
        ZoomAuth.objects.first().update_credentials(client_id, client_secret)
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


def manual_check(request):
    template = loader.get_template('main/manual-check.html')
    students = Student.objects.order_by('-email')
    context = {
        'students': students,
    }
    if request.method == "POST":
        print(request.POST)
        # a = Student(id=int(students[0].) + 1, name=request.POST['student-name'])
        # a.save()
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
