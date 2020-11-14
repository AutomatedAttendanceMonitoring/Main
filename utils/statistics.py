from autoAttendanceMonitoring.models import IsPresent, Student, Lesson, Subject


def lesson_statistics():
    for lesson in Lesson.objects.all():
        if lesson.statistics is None:
            lesson.statistics = len(IsPresent.objects.get(lesson=lesson.id)) / len(
                Student.objects.get(year_of_education=lesson.subject.year))
    for student in Student.objects.all():
        if student.statistics is None:
            total = 0
            for subject in Subject.objects.get(year=student.year_of_education):
                total += len(Lesson.objects.get(subject=subject))
            student.statistics = len(IsPresent.objects.get(student=student)) / total
