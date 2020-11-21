import re
from enum import Enum, unique

import requests

from autoAttendanceMonitoring.models import ZoomAuth


@unique
class ZoomError(Enum):
    SUCCESS = 0
    NO_TOKEN = 1
    INVALID_EMAIL = 2
    EMPTY_MESSAGE = 3
    USER_NOT_FOUND = 1001
    SENDING_ERROR = 5301
    INVALID_MEETING_ID = 3001
    MEETING_ACCESS_DENIED = 300


class Zoom:
    def __init__(self, auth: ZoomAuth):
        self.__auth = auth

    def send_message(self, emails: list[str], message_text: str) -> list[(ZoomError, dict)]:
        email_regex = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")
        if self.__auth is None or self.__auth.token is None:
            return [ZoomError.NO_TOKEN, dict()]
        elif message_text is None or message_text == "":
            return [ZoomError.EMPTY_MESSAGE, dict()]

        url = "https://api.zoom.us/v2/chat/users/me/messages"
        result = []
        for email in emails:
            if email_regex.fullmatch(email):
                response: dict = requests.post(url, data=f'{{"message": "{message_text}","to_contact":"{email}"}}', headers={
                    'content-type': "application/json",
                    'authorization': f"Bearer {self.__auth.token}"
                }).json()
                result.append((ZoomError(response.get("code", 0)), response | {"email": email}))
            else:
                result.append((ZoomError.INVALID_EMAIL, {"email": email}))
        return result

    # def list_participants(self, meeting_id: str) -> list[(ZoomError, dict)]:
    #     if self.__auth is None or self.__auth.token is None:
    #         return [ZoomError.NO_TOKEN, dict()]
    #
    #     url = f"https://api.zoom.us/v2/metrics/meetings/{meeting_id}/participants?page_size=300"
    #     return [(ZoomError.MEETING_ACCESS_DENIED, dict())]
