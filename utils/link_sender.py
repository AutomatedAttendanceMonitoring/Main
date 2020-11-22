from autoAttendanceMonitoring.models import Lesson, Student, ZoomAuth
from utils.Zoom import Zoom
from utils.db_commands import add_student_link
from utils.link_generator import LinkGenerator


def send_link_to(base_url: str, student: Student, lesson_id: str):
    print(student.__dict__)

    lesson = Lesson.objects.get(id=lesson_id)
    link = LinkGenerator.get_link(base_url, student)
    print(link)
    add_student_link(link=link, student=student, lesson=lesson)

    zoom = Zoom(ZoomAuth.objects.first())
    # print out the status of the message sending
    print(zoom.send_message([student.email], link)[0])



