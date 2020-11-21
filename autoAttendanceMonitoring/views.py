from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
import json

from autoAttendanceMonitoring.models import Student, IsPresent, ZoomAuth, ZoomParticipants
from utils.Zoom import Zoom, ZoomError
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
    zoom = Zoom(ZoomAuth.objects.first())
    results = zoom.send_message(request.GET.get("users", "").split(","), request.GET.get("message"))
    responses = {
        ZoomError.SUCCESS: "Message sent successfully; %",
        ZoomError.NO_TOKEN: f"Error: Zoom token is not present. Go to https://{request.get_host()}{reverse('zoom-set-credentials')} "
                            "passing your client_id and client_secret values as query parameters.",
        ZoomError.INVALID_EMAIL: "Email specified is not valid. %",
        ZoomError.EMPTY_MESSAGE: "Error: the message is empty.",
        ZoomError.USER_NOT_FOUND: "Error: the user either does not exist or not in the contact list. %",
        ZoomError.SENDING_ERROR: "Error: unable to send the message. %",
    }
    output = ""
    for status, data in results:
        output += responses[status].replace("%", str(data)) + "\n"

    return HttpResponse(f"<pre>{output}</pre>")


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


@csrf_exempt
def joined_left_participant(request):
    event: dict = json.loads(request.body)
    record = {
        "meeting_id": str(event["payload"]["object"]["id"]),
        "email": ''.join(event["payload"]["object"]["participant"]["user_name"].split())
    }
    if event.get("event") == "meeting.participant_joined":
        ZoomParticipants.objects.update_or_create(defaults=record)
    elif event.get("event") == "meeting.participant_left":
        ZoomParticipants.objects.filter(**record).delete()
    return HttpResponse()
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

