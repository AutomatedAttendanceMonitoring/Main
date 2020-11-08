from autoAttendanceMonitoring.models import AttendanceLink, Lesson, Student, IsPresent
from utils.db_commands import add_student_link
from utils.link_generator import LinkGenerator


def send_link_to(student: Student, lesson: Lesson):
    print(student.__dict__)
    link = LinkGenerator.get_link("http://127.0.0.1:8000/markattendance/", student)
    # TODO: sending link to zoom pc
    add_student_link(link=link, student=student, lesson=lesson)


def set_present(lesson: Lesson, student: Student):
    IsPresent.objects.create(student=student, lesson=lesson)

