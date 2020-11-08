from autoAttendanceMonitoring.models import Student, YearOfEducation, AttendanceLink, Lesson, IsPresent


def add_student(email: str, FName: str, LName: str, year_of_education: YearOfEducation):
    Student.objects.create(email=email, FName=FName, LName=LName, year_of_education=year_of_education)


def get_student_by_email(email: str) -> Student:
    return Student.objects.get(email=email)


def get_student_by_link_parameter(link_parameter: str) -> Student:
    param = AttendanceLink.objects.get(link_parameter=link_parameter)
    return param.student


def get_lesson_by_link_parameter(link_parameter: str) -> Student:
    param = AttendanceLink.objects.get(link_parameter=link_parameter)
    return param.lesson


def mark_student_attendance(link_parameter: str):
    student = get_student_by_link_parameter(link_parameter)
    lesson = get_lesson_by_link_parameter(link_parameter)
    IsPresent.objects.create(student=student, lesson=lesson)


def add_student_link(link: str, student: Student, lesson: Lesson):
    AttendanceLink.objects.create(link_parameter=link, student=student, lesson=lesson)
