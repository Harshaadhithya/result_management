from django.db import models
import uuid

from django.db.models.deletion import CASCADE
from users.models import Profile,Department

import datetime

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+4)]

def year_choices_for_semester():
    return [(r,r) for r in range(datetime.date.today().year-4, datetime.date.today().year+4)]

# Create your models here.

class Subject(models.Model):
    name=models.CharField(max_length=20,unique=True)
    subject_expansion=models.CharField(max_length=100,null=True)
    credit=models.IntegerField(default=0,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.subject_expansion

    class Meta:
        ordering=['name']
        

class Semester(models.Model):
    season_types=(
        ('odd','odd'),
        ('even','even')
    )
    semester_name=models.CharField(max_length=15,unique=True)
    year=models.IntegerField(default=datetime.date.today().year, choices=year_choices())
    season=models.CharField(max_length=30,choices=season_types,null=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.semester_name


class SemPapers(models.Model):
    semester=models.ForeignKey(Semester,on_delete=CASCADE,null=True,blank=True)
    dept=models.ForeignKey(Department,on_delete=CASCADE)
    batch=models.IntegerField(default=datetime.date.today().year, choices=year_choices_for_semester())
    subjects=models.ManyToManyField(Subject,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return "{}-{}-Batch{}".format(self.semester,self.dept,self.batch)

    class Meta:
        unique_together=('dept','semester','batch')
        ordering=['-semester__year','semester__season','dept']


class Result(models.Model):
    grade_choice=(
        ('O','O'),('A','A'),('B','B'),('C','C'),('D','D'),('E','E')
    )
    status_choice=(
        (True,'Pass'),
        (False,'Fail')
    )
    student=models.ForeignKey(Profile,on_delete=models.CASCADE)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True,blank=True)
    subject=models.ForeignKey(Subject,null=True,on_delete=models.SET_NULL)
    credit=models.IntegerField(default=0,null=True,blank=True)
    grade=models.IntegerField(default=0,null=True,blank=True)
    grade_string=models.CharField(max_length=2,null=True,choices=grade_choice)
    status=models.BooleanField(default=0,choices=status_choice)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)


    def __str__(self):
        return "{}-{}-{}".format(self.student,self.semester,self.subject)

    class Meta:
        unique_together=('student','semester','subject')
        constraints = [
            models.UniqueConstraint(
                fields=('student','semester','subject'),
                name='unique for student subject and semester'
            )]

class ResultCsv(models.Model):
    file_name=models.FileField(upload_to='csvfiles/')
    activated=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return "File-id:{},File-name:{}".format(self.id,self.file_name)

class FinalResult(models.Model):
    student=models.ForeignKey(Profile,on_delete=models.CASCADE)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True,blank=True)
    cgpa=models.FloatField(default=0,null=True,blank=True)
    total_credits=models.IntegerField(default=0)
    no_of_arrears=models.IntegerField(default=0)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    def __str__(self):
        return "{}-{}".format(self.student,self.semester)

    class Meta:
        unique_together=('student','semester')
        ordering=['student__roll_no','-semester__year']



