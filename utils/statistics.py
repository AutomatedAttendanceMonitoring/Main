from autoAttendanceMonitoring.models import IsPresent, Student, Lesson


def lesson_statistics(lesson_id):
    return len(IsPresent.objects.filter(lesson=lesson_id))


def student_statistics(email):
    return len(IsPresent.objects.filter(student=email))
