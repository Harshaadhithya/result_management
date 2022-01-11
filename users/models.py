from os import name
from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]





# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=200,unique=True)
    dept_expansion=models.CharField(max_length=200,unique=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.name
    class Meta:
        ordering=['name']

class Profile(models.Model):
    roles_type=(
        ('admin','admin_user'),
        ('student','student_user')
    )
    gender_type=(
        ('M','Male'),
        ('F','Female')
    )
   
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200)
    
    role=models.CharField(max_length=100,choices=roles_type)
    roll_no=models.CharField(max_length=15,unique=True)
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,blank=True,null=True)
    batch=models.IntegerField(default=datetime.date.today().year, choices=year_choices())
    profile_img=models.ImageField(null=False,blank=False,upload_to='profiles/',default='profiles/user-default.jpg')
    address=models.TextField(null=True,blank=True)
    dob=models.DateField(null=True)
    gender=models.CharField(max_length=10,choices=gender_type,null=True)
    mobile=models.IntegerField(null=True)
    verified=models.BooleanField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.roll_no

    class Meta:
        ordering=['-batch','dept','roll_no','verified']



