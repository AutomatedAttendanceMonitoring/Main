from autoAttendanceMonitoring.models import IsPresent, Student, Lesson


def lesson_statistics():
    for lesson in Lesson.objects.all():
        if lesson.statistics is None:
            lesson.statistics = len(IsPresent.objects.get(lesson=lesson.id))
    for student in Student.objects.all():
        if student.statistics is None:
            student.statistics = len(IsPresent.objects.get(student=student))
