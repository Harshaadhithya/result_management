from os import name
from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200)
    roll_no=models.CharField(max_length=15,unique=True)
    dept=models.ForeignKey(Department,on_delete=models.CASCADE,blank=True,null=True)
    year_of_study=models.IntegerField(default=1,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.roll_no



