from django.db.models import fields
from django.forms import ModelForm
from django.forms.forms import Form

from users.models import Department, Profile
from .models import Result,FinalResult,Semester,Subject,SemPapers
from django import forms
import datetime


class SubjectForm(ModelForm):
    class Meta:
        model=Subject
        fields='__all__'
        labels={'name':'Subject Code','subject_expansion':'Subject Name'}

    def __init__(self,*args,**kwargs):
        super(SubjectForm,self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['subject_expansion'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['credit'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})


class SemesterForm(ModelForm):
    class Meta:
        model=Semester
        fields=['year','season']

    def __init__(self,*args,**kwargs):
        super(SemesterForm,self).__init__(*args,**kwargs)
        self.fields['year'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})
        self.fields['season'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})


class SemPapersForm(ModelForm):
    class Meta:
        model=SemPapers
        fields='__all__'

        widgets={
            'subjects':forms.CheckboxSelectMultiple()
            }
    def __init__(self,*args,**kwargs):
        super(SemPapersForm,self).__init__(*args,**kwargs)
        self.fields['semester'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})
        self.fields['dept'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})
        self.fields['batch'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})

        

class ResultForm(ModelForm):
    class Meta:
        model=Result
        fields=['grade','status']
    def __init__(self,*args,**kwargs):
        super(ResultForm,self).__init__(*args,**kwargs)
        self.fields['grade'].widget.attrs.update({'class':'form-control','id':'formGroupExampleInput'})
        self.fields['status'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})

class admin_result_form(forms.Form):
    batch_choices=((r,r) for r in range(datetime.date.today().year-4, datetime.date.today().year+1))
    q1=Semester.objects.all()
    q2=Department.objects.all()
    dept=forms.ModelChoiceField(queryset=q2)
    semester=forms.ModelChoiceField(queryset=q1)
    batch=forms.ChoiceField(choices=batch_choices)

class FinalResultForm(forms.Form):
    batch_choices=((r,r) for r in range(1984, datetime.date.today().year+1))
    q2=Department.objects.all()
    q1=Semester.objects.all()
    department=forms.ModelChoiceField(queryset=q2)
    semester=forms.ModelChoiceField(queryset=q1)
    batch=forms.ChoiceField(choices=batch_choices)

    def __init__(self,*args,**kwargs):
        super(FinalResultForm,self).__init__(*args,**kwargs)
        self.fields['department'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})
        self.fields['semester'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})
        self.fields['batch'].widget.attrs.update({'class':'form-control form-select','id':'formGroupExampleInput'})


