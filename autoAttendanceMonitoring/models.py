from django.db import models
from base64 import b64encode
from datetime import datetime, timedelta
import pytz
import requests
import uuid


class ZoomAuth(models.Model):
    active_token = models.CharField(max_length=700, default="")
    refresh_token = models.CharField(max_length=700, default="")
    expires_at = models.DateTimeField('expiration time', default=datetime.fromtimestamp(0))
    client_id = models.CharField(max_length=25)
    client_secret = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.expires_at.strftime("Token (expires at %d/%m/%Y %H:%M:%S)")

    @property
    def token(self) -> str:
        """
        Get an active token. If the current one is expired, obtain the new one.
        :return: Current active token or None if it needs to be obtained manually
        """
        if self.refresh_token is not None and pytz.UTC.localize(datetime.now()) >= self.expires_at:
            self.refresh_oauth()
        return self.active_token

    def new_token(self, oauth_code: str, redirect_uri: str) -> None:
        """
        Update current OAuth using the code obtained after first authorization
        :param oauth_code: code returned by Zoom API
        :param redirect_uri: redirect uri used to obtain the code
        :return: True on successful refresh
        """
        client_info = b64encode(self.client_id.encode("utf-8") + b':' + self.client_secret.encode("utf-8")).decode("utf-8")
        response = requests.post(f"https://zoom.us/oauth/token?redirect_uri={redirect_uri}&grant_type=authorization_code&code={oauth_code}", headers={
            "Authorization": f"Basic {client_info}"
        }).json()
        self.active_token = response.get("access_token")
        self.refresh_token = response.get("refresh_token")
        self.expires_at = datetime.now() + timedelta(seconds=response.get("expires_in"))
        self.save()
        return self.active_token is not None

    def refresh_oauth(self) -> bool:
        """
        Refresh current OAuth using the refresh token received after the first authorization
        :return: True on successful refresh
        """
        client_info = b64encode(self.client_id.encode("utf-8") + b':' + self.client_secret.encode("utf-8")).decode("utf-8")
        response = requests.post("https://zoom.us/oauth/token?grant_type=refresh_token&refresh_token=", headers={
            "Authorization": f"Basic {client_info}"
        }).json()
        self.active_token = response.get("access_token")
        self.refresh_token = response.get("refresh_token")
        self.expires_at = datetime.now() + timedelta(seconds=response.get("expires_in"))
        self.save()
        return self.active_token is not None


class YearOfEducation(models.Model):
    number = models.CharField(primary_key=True, max_length=10)


class Student(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    FName = models.CharField(max_length=50)
    LName = models.CharField(max_length=50)
    year_of_education = models.ForeignKey(YearOfEducation, models.DO_NOTHING)
    statistics = models.IntegerField(default=None)


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    year = models.ForeignKey(YearOfEducation, models.DO_NOTHING)


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    kind = models.CharField(max_length=10)
    subject = models.ForeignKey(Subject, models.DO_NOTHING)
    statistics = models.IntegerField(default=None)


class IsTaughtBy(models.Model):
    subject = models.ForeignKey(Subject, models.DO_NOTHING)
    instructor = models.ForeignKey(Lesson, models.DO_NOTHING)


class IsPresent(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING)
    lesson = models.ForeignKey(Lesson, models.DO_NOTHING)


class AttendanceLink(models.Model):
    link_parameter = models.CharField(max_length=256, primary_key=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    lesson = models.ForeignKey(Lesson, models.DO_NOTHING)
