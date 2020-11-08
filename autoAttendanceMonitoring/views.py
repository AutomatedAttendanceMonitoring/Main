from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from .models import Student

def index(request):
    return render(request, 'main/main-page.html')

def manual_check(request):
    template = loader.get_template('main/manual-check.html')
    students = Student.objects.order_by('-id')
    context = {
        'students' : students,
    }
    if request.method == "POST":
        print(request.POST)
        a = Student(id=int(students[0].id)+1, name=request.POST['student-name'])
        a.save()
        return HttpResponseRedirect("/manual-check")
    return HttpResponse(template.render(context,request))


def mark_read(request):
    pass