import json
import re
from datetime import datetime

from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth

from autoAttendanceMonitoring.models import Lesson, Subject
from autoAttendanceMonitoring.models import Student, IsPresent, ZoomAuth, ZoomParticipants
from utils import statistics
from utils.Zoom import Zoom, ZoomError
from utils.db_commands import mark_student_attendance
from utils.link_sender import send_link_to
from utils.services.export_to_csv import CsvService


def index(request):
    template = loader.get_template('main/main-page.html')
    lessons = Lesson.objects.all()
    context = {
        'lessons': lessons
    }
    if request.method == "POST":
        parsed_link = re.search(r"/(?P<id>\d+)\?", request.POST['zoom-link'])
        if parsed_link is None:
            return HttpResponseBadRequest("<pre>Error: Zoom link is not valid.</pre>")
        else:
            return redirect(f"/send_links/{request.POST['select-lesson']}?meeting={parsed_link.group('id')}")
    return HttpResponse(template.render(context, request))


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
        return HttpResponseBadRequest("Error: client_id and client_secret are required\n")
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
    return HttpResponse(
        "Obtained new tokens successfully\n" if success else "Error obtaining new tokens, yet client info was saved")


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
    template = loader.get_template('main/log-in.html')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            # redirect to the page with list of all lessons
            return HttpResponse("/")
        else:
            return HttpResponse(template.render())
    return HttpResponse(template.render())


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
            statistics=0,
        )
        lesson.save()
        return redirect("/select-lesson")
    return HttpResponse(template.render(context, request))


def manual_check(request, lesson_id):
    template = loader.get_template('main/manual-check.html')
    lesson = Lesson.objects.get(pk=lesson_id)

    marked_students = [record.student for record in list(IsPresent.objects.filter(lesson_id=lesson_id))]
    students = Student.objects.filter(year_of_education=lesson.subject.year)
    context = {
        'students': students,
        'marked_students': marked_students,
        'lesson': lesson
    }
    if request.method == "POST":
        print(request.POST)
        student = Student.objects.get(pk=request.POST['select-student'])
        present = IsPresent(
            student=student,
            lesson_id=lesson_id
        )
        present.save()
        return redirect(f"/manual-check/{lesson_id}")
    return HttpResponse(template.render(context, request))


def mark_student(request, link_parameter):
    if request.method not in ["GET", "POST"] or request.META.get('HTTP_USER_AGENT', '').find("Zoom") != -1:
        return HttpResponse("Open the page to mark your attendance")
    template = loader.get_template('main/attendance-marked.html')
    success = False
    try:
        mark_student_attendance(f"{request.scheme}://{request.get_host()}/markattendance/{link_parameter}")
        success = True
    except:
        pass
    context = {
        'success': success
    }
    return HttpResponse(template.render(context, request))


def send_links(request, lesson_id):
    base_url = f"{request.scheme}://{request.get_host()}/markattendance/"
    try:
        for entry in ZoomParticipants.objects.filter(meeting_id=request.GET['meeting']):
            try:
                student = Student.objects.get(email=entry.email)
                send_link_to(base_url, student, lesson_id)
            except Student.DoesNotExist:
                pass
        return redirect(f"/manual-check/{lesson_id}")
    except Exception:
        return HttpResponse("500 server error")


def export_to_csv(request, path):
    CsvService.export_from_db(IsPresent, path)
    return HttpResponse("200 OK")


def show_stats_for_lesson(request, lesson_id):
    data = {"present": statistics.lesson_statistics(lesson_id),
            "total": len(Student.objects.filter(year_of_education=Lesson.objects.get(id=lesson_id).subject.year))}
    return render(request, "main/Stats.html", context=data)


def show_stats_for_student(request, email):
    total = 0
    for subject in Subject.objects.filter(year=Student.objects.get(email=email).year_of_education):
        total += len(Lesson.objects.filter(subject=subject))
    data = {"present": statistics.student_statistics(email), "total": total}
    return render(request, "main/Stats.html", context=data)
