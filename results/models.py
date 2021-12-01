from django.db import models
import uuid

from django.db.models.deletion import CASCADE
from users.models import Profile,Department

# Create your models here.

class Subject(models.Model):
    name=models.CharField(max_length=20)
    credit=models.IntegerField(default=0,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.name

class Semester(models.Model):
    semester_name=models.CharField(max_length=15)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.semester_name



class SemPapers(models.Model):
    semester=models.ForeignKey(Semester,on_delete=CASCADE,null=True,blank=True)
    dept=models.ForeignKey(Department,on_delete=CASCADE)
    paper=models.ForeignKey(Subject,on_delete=CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.paper.name


class Result(models.Model):
    student=models.ForeignKey(Profile,on_delete=models.CASCADE)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE,null=True,blank=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    credit=models.IntegerField(default=0,null=True,blank=True)
    grade=models.IntegerField(default=0,null=True,blank=True)
    status=models.BooleanField()
    cgpa=models.IntegerField(default=0,null=True,blank=True)
    sgpa=models.IntegerField(default=0,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)


    def __str__(self):
        return self.student.roll_no