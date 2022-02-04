from django.contrib import admin
from .models import Subject,Semester,Result,FinalResult,SemPapers,ResultCsv
# Register your models here.

admin.site.register(Subject)
admin.site.register(Semester)
admin.site.register(Result)
admin.site.register(SemPapers)
admin.site.register(FinalResult)
admin.site.register(ResultCsv)
