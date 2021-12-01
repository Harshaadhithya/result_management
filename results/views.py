from django.shortcuts import render
from .models import SemPapers,Semester,Subject,Result
# Create your views here.

def result_home(request):
    semesters=Semester.objects.all()
    context={'semesters':semesters}
    return render(request,'results/result_home.html',context)

def results(request,pk):
    student_id='48b0bb52-eefa-4e05-8bf9-fe9953e569c2'
    current_sem=Semester.objects.get(id=pk)
    results=Result.objects.filter(student=student_id,semester=pk)
    context={'results':results,'current_sem':current_sem}
    return render(request,'results/result.html',context)