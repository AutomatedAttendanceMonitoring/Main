from autoAttendanceMonitoring.models import Student, AttendanceLink, Lesson, IsPresent
from utils.moodleAPI import import_to_moodle


def add_student(email: str, FName: str, LName: str, year_of_education_id: str):
    Student.objects.create(email=email, FName=FName, LName=LName, year_of_education_id=year_of_education_id)


def get_student_by_email(email: str) -> Student:
    return Student.objects.get(email=email)


def get_student_by_link_parameter(link_parameter: str) -> Student:
    param = AttendanceLink.objects.get(link_parameter=link_parameter)
    return param.student


def get_lesson_by_link_parameter(link_parameter: str) -> Lesson:
    param = AttendanceLink.objects.get(link_parameter=link_parameter)
    return param.lesson


def mark_student_attendance(link_parameter: str):
    student = get_student_by_link_parameter(link_parameter)
    lesson = get_lesson_by_link_parameter(link_parameter)
    set_present(lesson, student)
    import_to_moodle(lesson.start_time, lesson.start_time, lesson.kind, student.email)


def set_present(lesson: Lesson, student: Student):
    is_present = IsPresent(lesson=lesson, student=student)
    is_present.save()


def add_student_link(link: str, student: Student, lesson: Lesson):
    print("not error 1")
    alink = AttendanceLink(link_parameter=link, student=student, lesson=lesson)
    print("not error 2")
    print(alink.__dict__)
    alink.save()
    print("not error 3")
