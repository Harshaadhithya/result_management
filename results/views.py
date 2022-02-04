from distutils.log import error
from enum import unique
from django import contrib
from django.db.models import fields
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render

from results.forms import SubjectForm,SemesterForm,ResultForm,SemPapersForm,admin_result_form,FinalResultForm,csv_form
from .models import FinalResult,Semester,Subject,Result,SemPapers
from users.models import Department,Profile
from django.forms import inlineformset_factory
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.db.models import Q

import csv,io

#checked
@login_required(login_url='login')
def subject(request):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        search_query=''
        if request.GET.get('search_query'):
            search_query=request.GET.get('search_query')
            
        subjects=Subject.objects.distinct().filter(
            Q(name__icontains=search_query)|
            Q(subject_expansion__icontains=search_query)
            )
        context={'subjects':subjects,'search_query':search_query}
        return render(request,'results/subject.html',context)
    else:
        messages.error(request,'Only Verified Admin Users can access this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def create_subject(request):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:

        profile=request.user.profile
        
        form=SubjectForm()
        context={'form':form}
        if request.method=='POST':
            form=SubjectForm(request.POST)
            if form.is_valid():
                subject=form.save(commit=False)
                subject.name=subject.name.lower()
                subject.save()
                return redirect('subject')
        return render(request,'results/subject_form.html',context)
    else:
        messages.error(request,'Only Verified Admin Users can access this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def update_subject(request,pk):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        subject=Subject.objects.get(id=pk)
        form=SubjectForm(instance=subject)
        if request.method=='POST':
            form=SubjectForm(request.POST,instance=subject)
            if form.is_valid():
                form.save()
            else:
                messages.error(request,"Something went wrong!")
            return redirect('subject')
        context={'form':form}
        return render(request,'results/subject_form.html',context)
    else:
        messages.error(request,'Only Verified Admin Users can access this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def semester(request):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:

        semesters=Semester.objects.all()
        context={'semesters':semesters}
        return render(request,'results/semester.html',context)
    else:
        messages.error(request,'Only Verified Admin Users can access this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def create_sem(request):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        form=SemesterForm()
        context={'form':form}
        if request.method=='POST':
            form=SemesterForm(request.POST)
            
            if form.is_valid():
                try:
                    semester=form.save(commit=False)
                    semester.semester_name=str(semester.year)+'-'+str(semester.season)
                    semester.save()
                except:
                       messages.error(request,"Semester already Exists") 
                return redirect('semester')
            
        return render(request,'results/sem_form.html',context)
    else:
        messages.error(request,'Only Verified Admin Users can access this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def update_sem(request,pk):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:    
        semester=Semester.objects.get(id=pk)
        form=SemesterForm(instance=semester)
        context={'form':form}
        if request.method=='POST':
            form=SemesterForm(request.POST,instance=semester)
            if form.is_valid():
                form.save()
            else:
                messages.error(request,"Something went wrong!")
            return redirect('semester')
        return render(request,'results/sem_form.html',context)
    else:
        messages.error(request,'Only Admin users have access to this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def students_result_home(request):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:    
        form=FinalResultForm()
        if request.method=='POST':
            
            request.session['batch1']=request.POST['batch']
            request.session['department1']=request.POST['department']
            request.session['semester1']=request.POST['semester']
            return redirect('students_result')
        context={'form':form}
        return render(request,'results/create_result_home_form.html',context)
    else:
        messages.error(request,'Only admin users have access to this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def students_result(request):
    page='students_result'
    if request.user.profile.role=='admin' and request.user.profile.verified==True:    
        dept_obj=Department.objects.get(id=request.session.get('department1'))
        semester_obj=Semester.objects.get(id=request.session.get('semester1'))
        batch_obj=request.session.get('batch1')

        students=Profile.objects.filter(dept=dept_obj,batch=batch_obj)
        sempapers=SemPapers.objects.filter(semester=semester_obj,dept=dept_obj,batch=batch_obj)
        final_results_list=FinalResult.objects.filter(student__dept=dept_obj,student__batch=batch_obj,semester=semester_obj)
        final_results_students=final_results_list.values_list('student',flat=True)
        if len(sempapers)==0:
            messages.error(request,f"{semester_obj} is not yet assigned for {dept_obj}")
            return redirect('home')
        unupdated_stduents=[]
        for student in students:
            if student.id not in final_results_students:
                unupdated_stduents.append(student)
        context={'page':page,'final_results_list':final_results_list,'semester':semester_obj,'dept':dept_obj,'batch':batch_obj,'unupdated_students':unupdated_stduents}
        return render(request,'results/students_result.html',context)

    else:
        messages.error(request,'Only admin users have access to this!')
        return redirect('home')

@login_required(login_url='login')
def my_results(request):
    profile=request.user.profile
    page='my_result'
    if profile.role=='student':
        final_results=FinalResult.objects.filter(student=profile)
        context={'final_results':final_results,'page':page}
        return render(request,'results/students_result.html',context)
    else:
        messages.error("No Results to Show!")
        return redirect('home')



#checked
def delete_result(request,pk):
    final_result=FinalResult.objects.get(id=pk)
    student=final_result.student
    semester=final_result.semester
    results=Result.objects.filter(student=student,semester=semester)
    results.delete()
    final_result.delete()
    return redirect('students_result')


#check once again
@login_required(login_url='login')
def results(request,pk):
    profile=request.user.profile
    student_id=profile.id
    
    current_sem=Semester.objects.get(id=pk)
    results=Result.objects.filter(student=student_id,semester=pk)
    final_result=FinalResult.objects.get(student=student_id,semester=pk)
    context={'student':profile,'results':results,'current_sem':current_sem,'final_result':final_result}
    return render(request,'results/result.html',context)

#checked
@login_required(login_url='login')
def admin_result_view(request,pk):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:    
        final_result_id=pk
        final_result_obj=FinalResult.objects.get(id=final_result_id)
        student_obj=final_result_obj.student
        semester_obj=final_result_obj.semester
        current_sem=semester_obj
        results=Result.objects.filter(student=student_obj,semester=semester_obj)
        context={'semester':semester_obj,'student':student_obj,'results':results,'current_sem':current_sem,'final_result':final_result_obj}
        return render(request,'results/result.html',context)
    else:
        messages.error(request,'Only Admin users have access to this!')
        return redirect('home')


#checked
@login_required(login_url='login')
def create_final_result(student_obj,sem_obj,arrear_count,tot_credits,grade_list):
    cgpa=sum(grade_list)/len(grade_list)
    print(student_obj,sem_obj,arrear_count,tot_credits,grade_list,cgpa)
    try:
        FinalResult.objects.create(student=student_obj,semester=sem_obj,cgpa=cgpa,no_of_arrears=arrear_count,total_credits=tot_credits)
    except:
        return redirect('home')


#checked
@login_required(login_url='login')
def create_result(request,pk):
    page='create'
    if request.user.profile.role=='admin' and request.user.profile.verified==True:    

        student_obj=Profile.objects.get(id=pk)
        semester_id=request.session.get('semester1')
        semester_obj=Semester.objects.get(id=semester_id)
        dept_obj=student_obj.dept
        batch_obj=student_obj.batch
        try:
            sem_papers_obj=SemPapers.objects.get(semester=semester_obj,dept=dept_obj,batch=batch_obj)
            
        except:
            messages.error(request,"No semester is assigned till now")
            return redirect('home')
        subjects=sem_papers_obj.subjects.all()
        ResultFormSet=inlineformset_factory(Profile,Result,fields=('subject','grade'), extra=len(subjects)+3,can_delete=False)

        formset=ResultFormSet(queryset=Result.objects.none())
        try:
            for index,form in enumerate(formset):
                form['subject'].initial=subjects[index]
        except:
            pass    
        if request.method=='POST':
            
            arrear_count=0
            tot_credits=0
            grade_list=[]
            formset=ResultFormSet(request.POST,instance=student_obj)
            if formset.is_valid():
                instances=formset.save(commit=False)
                for instance in instances:
                    instance.semester=semester_obj
                    sub_credit=instance.subject.credit
                    
                    grade_list.append(instance.grade)
                    if instance.grade>=5:
                        instance.credit=sub_credit
                        tot_credits+=sub_credit
                        instance.status=True
                        if instance.grade>=9:
                            instance.grade_string='O'
                        elif instance.grade==8:
                            instance.grade_string='A'
                        elif instance.grade==7:
                            instance.grade_string='B'
                        elif instance.grade==6:
                            instance.grade_string='C'
                        else:
                            instance.grade_string='D'
                    else:
                        instance.credit=0
                        instance.status=False
                        arrear_count+=1
                        instance.grade_string='E'
                    try:
                        instance.save()
                        
                    except:
                        messages.error(request,"Result already Exist!")
                create_final_result(student_obj,semester_obj,arrear_count,tot_credits,grade_list)
                messages.success(request,"Result Created Successfully !")
                return redirect('students_result')
                
        context={'formset':formset,'subjects':subjects,'sem_obj':semester_obj,'student_obj':student_obj,'page':page}
        return render(request,'results/create_result_form.html',context)
    else:
        messages.error(request,'Only verified Admin users have access to this!')
        return redirect('home')

def add_result_using_csv(myfile):
    error_messages=''
    unadded_students_list=[]
    
  
    with open(myfile.file_name.path,'r') as csvfile:
        csvreader=csv.reader(csvfile)
        head=next(csvreader)
        
        unadded_students=[]
        for row in csvreader:
            objs=[]
            arrear_count=0
            tot_credits=0
            grade_list=[]
            if len(row)>0:
                student_roll_no=row[0].lower()
            else:
                break
            semester_year,semester_season=row[1].split('-')
            try:
                student_obj=Profile.objects.get(roll_no=student_roll_no)
            except:
                error_messages+="this roll no:{} is not valid\n".format(student_roll_no)
                continue
            try:
                semester_obj=Semester.objects.get(year=semester_year,season=semester_season)
            except:
                unadded_students.append(student_obj.roll_no)
                continue
            subjects=row[2].split(',')
            for mark in subjects:
                subject_code,grade=mark.split('-')
                grade=int(grade)
                try:
                    subject_obj=Subject.objects.get(name=subject_code.lower())
                except:
                    error_messages+='{} is not a valid subject'.format(subject_code)
                    objs.clear()
                    unadded_students.append(student_obj.roll_no)
                    break
                grade_list.append(grade)
                if grade>=5:
                    credit=subject_obj.credit
                    tot_credits+=credit
                    status=True
                    if grade>=9:
                        grade_string='O'
                    elif grade==8:
                        grade_string='A'
                    elif grade==7:
                        grade_string='B'
                    elif grade==6:
                        grade_string='C'
                    else:
                        grade_string='D'

                else:
                    credit=0
                    status=False
                    arrear_count+=1
                    grade_string='E'
                
                objs.append(Result(student=student_obj,semester=semester_obj,subject=subject_obj,credit=credit,grade=grade,grade_string=grade_string,status=status)) 
            try:
                if len(objs)>0:       
                    Result.objects.bulk_create(objs=objs)
                    FinalResult.objects.create(student=student_obj,semester=semester_obj,cgpa=sum(grade_list)/len(grade_list),no_of_arrears=arrear_count,total_credits=tot_credits)
            except:
                unadded_students.append(student_obj.roll_no)
    if len(unadded_students)>0:
        error_messages+="\nThe following student's result has not been added"
        for student in unadded_students:
            error_messages+="{},".format(student)
    return error_messages

@login_required(login_url='login')
def csv_upload(request):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        form=csv_form()
        if request.method=='POST':
            form=csv_form(request.POST,request.FILES)
            if form.is_valid():
                if request.FILES['file_name'].name.endswith('.csv'):
                    myfile=form.save()
                    error_messages=add_result_using_csv(myfile)
                    if len(error_messages)==0:
                        messages.success(request,'Results added successfully')
                    else:
                        messages.warning(request,error_messages)
                    return redirect('students_result')
                else:
                    messages.error(request,'File Format must be CSV')  
                    return redirect('students_result') 
        context={'form':form}    
        return render(request,'results/csv_upload_form.html',context)
    else:
        messages.error(request,'Only verified Admin users have access to this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def update_result_view(request,pk):  
    if request.user.profile.role=='admin' and request.user.profile.verified==True:    
        student_obj=Profile.objects.get(id=pk)
        sem_obj=Semester.objects.get(id=request.session.get('semester1'))
        results=Result.objects.filter(student=student_obj,semester=sem_obj)
        final_result=FinalResult.objects.get(student=student_obj,semester=sem_obj)
        context={'student':student_obj,'semester':sem_obj,'results':results,'final_result':final_result}
        return render(request,'results/update_result_view.html',context)
    else:
        messages.error(request,'Only verified Admin users have access to this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def update_result(request,pk):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:    

        result=Result.objects.get(id=pk)
        page='update'
        form=ResultForm(instance=result)
        if request.method=='POST':
            form=ResultForm(request.POST,instance=result)
            if form.is_valid():
                form.save()
                results=Result.objects.filter(student=result.student,semester=result.semester)
                arrear_count=0
                tot_credits=0
                grade_list=[]
                for result in results:
                    grade_list.append(result.grade)
                    if result.status==False:
                        arrear_count+=1
                        result.credit=0
                        result.save()
                        result.grade_string='E'
                        result.save()

                    else:
                        result.credit=result.subject.credit
                        if result.grade>=9:
                            result.grade_string='O'
                        elif result.grade==8:
                            result.grade_string='A'
                        elif result.grade==7:
                            result.grade_string='B'
                        elif result.grade==6:
                            result.grade_string='C'
                        else:
                            result.grade_string='D'
                        result.save()
                        tot_credits+=result.subject.credit
                cgpa=sum(grade_list)/len(grade_list)
                final_result_obj=FinalResult.objects.get(student=result.student,semester=result.semester)
                final_result_obj.no_of_arrears=arrear_count
                final_result_obj.total_credits=tot_credits
                final_result_obj.cgpa=cgpa
                final_result_obj.save()
                return redirect('update_result_view',pk=result.student.id)
        context={'page':page,'form':form,'result':result}
        return render(request,'results/create_result_form.html',context)
    else:
        messages.error(request,'Only verified Admin users have access to this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def dept_sem_papers(request):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:   
        search_query=''
        if request.GET.get('search_query'):
            search_query=request.GET.get('search_query') 
        dept_sem_papers=SemPapers.objects.distinct().filter(Q(semester__semester_name__icontains=search_query)|Q(batch__icontains=search_query)|Q(dept__name__icontains=search_query)|Q(dept__dept_expansion__icontains=search_query))
        context={'dept_sem_papers':dept_sem_papers}
        return render(request,'results/dept_sem_papers.html',context)
    else:
        messages.error(request,'Only verified Admin users have access to this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def create_dept_sem_papers(request):
    profile=request.user.profile
    page='create'
    if request.user.profile.role=='admin' and request.user.profile.verified==True:   
        form=SemPapersForm()
        context={'form':form,'page':page}
        if request.method=='POST':
            form=SemPapersForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Subjects Assigned Successfully!")
                return redirect('dept_sem_papers')
            else:
                dept=Department.objects.get(id=request.POST['dept'])
                semester=Semester.objects.get(id=request.POST['semester'])
                messages.error(request,f"Subjects for {dept} for {semester} is assigned already! ")
                return redirect('dept_sem_papers')
        return render(request,'results/dept_sem_paper_form.html',context)
    else:
        messages.error(request,'Only verified Admin users have access to this!')
        return redirect('home')

#checked
@login_required(login_url='login')
def update_dept_sem_papers(request,pk):
    profile=request.user.profile
    page='update'
    if request.user.profile.role=='admin' and request.user.profile.verified==True:   
        sem_paper_obj=SemPapers.objects.get(id=pk)
        form=SemPapersForm(instance=sem_paper_obj)
        if request.method=='POST':
            form=SemPapersForm(request.POST,instance=sem_paper_obj)
            if form.is_valid():
                form.save()
                messages.success(request,"Subjects updated Successfully!")
                return redirect('dept_sem_papers')
        context={'form':form,'page':page}
        return render(request,'results/dept_sem_paper_form.html',context)
    else:
        messages.error(request,'Only verified Admin users have access to this!')
        return redirect('home')