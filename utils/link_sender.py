from autoAttendanceMonitoring.models import AttendanceLink, Lesson, Student, IsPresent
from utils.db_commands import add_student_link
from utils.link_generator import LinkGenerator


def send_link_to(student: Student, lesson_id: str):
    print(student.__dict__)

    lesson = Lesson.objects.get(id=lesson_id)
    link = LinkGenerator.get_link("http://127.0.0.1:8000/markattendance/", student)
    print(link)
    add_student_link(link=link, student=student, lesson=lesson)

    # TODO: sending link to zoom pc




