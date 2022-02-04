from django import forms
from django.db import models
from django.db.models import query
from django.forms import ModelForm
from .models import Profile,Department

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.admin.widgets import AdminDateWidget


import datetime

def year_choices():
    return [(r,r) for r in range(2000, datetime.date.today().year+1)]

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','email','username','password1','password2']
        labels={'first_name':'Name'}
    
    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'type':'text', 'name':'roll_no', 'class':'form-control'})
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'type':'text', 'name':'roll_no', 'class':'form-control'})
        self.fields['username'].widget.attrs.update({'type':'text', 'name':'roll_no', 'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'type':'password', 'name':'password', 'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'type':'password', 'name':'password', 'class':'form-control'})

class DepartmentForm(ModelForm):
    class Meta:
        model=Department
        fields='__all__'
        labels={'name':'Department Code','dept_expansion':'Department Name'}
    
    def __init__(self,*args,**kwargs):
        super(DepartmentForm,self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['dept_expansion'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})

class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields='__all__'
        exclude=['user','role']
    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        self.fields['roll_no'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['name'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['dept'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})
        self.fields['profile_img'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['batch'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['address'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['dob'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput','placeholder':'YYYY-MM-DD'})
        self.fields['gender'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})
        self.fields['mobile'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['verified'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})

        

class StudentUserForm(forms.Form):
    q1=Department.objects.all()
    q2=(
        ('M','Male'),
        ('F','Female')
    )
    q3=year_choices()
    roll_no=forms.CharField(max_length=30)
    full_name=forms.CharField(max_length=40)
    email=forms.EmailField()
    department=forms.ModelChoiceField(queryset=q1)
    profile_img=forms.ImageField()
    batch=forms.ChoiceField(choices=q3)
    address=forms.CharField(max_length=300,widget=forms.Textarea)
    dob=forms.DateField()
    gender=forms.ChoiceField(choices=q2)
    mobile=forms.IntegerField()

    def __init__(self,*args,**kwargs):
        super(StudentUserForm,self).__init__(*args,**kwargs)
        self.fields['roll_no'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['full_name'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['email'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['department'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})
        self.fields['profile_img'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['batch'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})
        self.fields['address'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['dob'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput','placeholder':'YYYY-MM-DD'})
        self.fields['gender'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})
        self.fields['mobile'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})


class AdminUserForm(forms.Form):
    q2=(
        ('M','Male'),
        ('F','Female')
    )
    
    profile_img=forms.ImageField()
    address=forms.CharField(max_length=300,widget=forms.Textarea)
    dob=forms.DateField()
    gender=forms.ChoiceField(choices=q2)
    mobile=forms.IntegerField()

    def __init__(self,*args,**kwargs):
        super(AdminUserForm,self).__init__(*args,**kwargs)
        self.fields['profile_img'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['address'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['dob'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput','placeholder':'YYYY-MM-DD'})
        self.fields['gender'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})
        self.fields['mobile'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})



    