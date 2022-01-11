
from re import T, search
from django import forms
from django.contrib import messages

from django.shortcuts import render,redirect
from .models import Profile,Department
from .forms import DepartmentForm,ProfileForm,StudentUserForm,CustomUserCreationForm,AdminUserForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.

def home(request):
    profiles=Profile.objects.all()
    context={'profiles':profiles}
    return render(request,'index.html',context)


@login_required(login_url='login')
def profile(request):
    profile=request.user.profile
    return render(request,'users/profile.html',{'profile':profile})




#checked
def user_login(request):
    page='login'
    context={'page':page}
    if request.method=='POST':
        entered_roll_no=request.POST['roll_no'].lower()
        entered_password=request.POST['password']
        try:
            user=User.objects.get(username=entered_roll_no)
        except:
            pass
        user=authenticate(request,username=entered_roll_no,password=entered_password)

        if user is not None:
            login(request,user)
            messages.success(request,"User Logged in")
            return redirect('home')
        else:
            messages.error(request,"Username or password worng!")
    return render(request,'users/login_form.html',context)

#checked
def dept(request):
    depts=Department.objects.all()
    context={'depts':depts}
    return render(request,'users/dept.html',context)

#checked
@login_required(login_url='login')
def create_dept(request):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        form=DepartmentForm()
        context={'form':form}
        if request.method=='POST':
            form=DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dept')
            else:
                messages.error(request,'Something went wrong!')
        return render(request,'users/dept_form.html',context)
    else:
        messages.error(request,"Only Verified Admin Users can access this!")
        return redirect('home')

#checked
@login_required(login_url='login')
def update_department(request,pk):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        dept=Department.objects.get(id=pk)
        form=DepartmentForm(instance=dept)
        if request.method=='POST':
            form=DepartmentForm(request.POST,instance=dept)
            if form.is_valid():
                form.save()
                return redirect('dept')
            else:
                messages.error(request,'Something went wrong!')
        context={'form':form}
        return render(request,'users/dept_form.html',context)
    else:
        messages.error(request,"Only Verified Admin Users can access this!")
        return redirect('home')

#checked
@login_required(login_url='login')
def students(request):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        search_query=''
        if request.GET.get('search_query'):
            search_query=request.GET.get('search_query')
        students=Profile.objects.distinct().filter(
            Q(role='student')&(
            Q(roll_no__icontains=search_query)|
            Q(dept__name__icontains=search_query)|
            Q(name__icontains=search_query)
            )
            )
        context={'students':students,'search_query':search_query}
        return render(request,'users/students.html',context)
    else:
        messages.error(request,"Only Verified Admin Users can access this!")
        return redirect('home')

#checked
@login_required(login_url='login')
def student_profile(request,pk):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        student=Profile.objects.get(id=pk)
        context={'profile':student}
        return render(request,'users/profile.html',context)
    else:
        messages.error(request,"Only Verified Admin Users can access this!")
        return redirect('home')

#checked
@login_required(login_url='login')
def edit_student_by_admin(request,pk):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        profile=Profile.objects.get(id=pk)
        form=ProfileForm(instance=profile)
        if request.method=='POST':
            form=ProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid():
                form.save()
                return redirect('students')
            else:
                messages.error(request,'Something went wrong!')
        context={'form':form}
        return render(request,'users/student_form.html',context)
    else:
        messages.error(request,"Only Verified Admin Users can access this!")
        return redirect('home')

#checked
@login_required(login_url='login')
def create_student(request):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        form=StudentUserForm
        context={'form':form}
        if request.method=='POST':
            roll_no=request.POST['roll_no'].lower()
            email=request.POST['email']
            name=request.POST['full_name']
            dept_id=request.POST['department']
            dept=Department.objects.get(id=dept_id)
            batch=request.POST['batch']
            gender=request.POST['gender']
            dob=request.POST['dob']
            address=request.POST['address']
            mobile=request.POST['mobile']
            profile_img=request.FILES['profile_img']
            try:
                user=User.objects.create_user(username=roll_no, email=email, password=roll_no)
                print(dob)
                student=Profile.objects.create(user=user,name=name,role='student',roll_no=roll_no,dept=dept,profile_img=profile_img,batch=batch,dob=dob,address=address,gender=gender,mobile=mobile,verified=True)
                student.save()
                messages.success(request,"Student Created successfully!")
                return redirect('students')
            except:
                messages.error(request,"Roll No already exists!")
                return redirect('create_user')
        return render(request,'users/create_user.html',context)
    else:
        messages.error(request,"Only Verified Admin Users can access this!")
        return redirect('home')

#checked
@login_required(login_url='login')
def admin_users(request):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        search_query=''
        if request.GET.get('search_query'):
            search_query=request.GET.get('search_query')
        admins=Profile.objects.distinct().filter(
            Q(role='admin')&(
            Q(name__icontains=search_query)
            )
        )
        context={'admins':admins,'search_query':search_query}
        return render(request,'users/admins.html',context)
    else:
        messages.error(request,"Only Verified Admin Users can access this!")
        return redirect('home')

#checked
@login_required(login_url='login')
def verify_admin(request,pk):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        admin=Profile.objects.get(id=pk)
        admin.verified=True
        admin.save()
        messages.success(request,"Verified Successfully!")
    else:
        messages.error(request,'Only Verified Admins can verify other users')
    
    return redirect('admin_users')

#checked
@login_required(login_url='login')
def delete_admin(request,pk):
    if request.user.profile.role=='admin' and request.user.profile.verified==True:
        admin=Profile.objects.get(id=pk)
        print(admin.verified)
        if admin.verified!=False:
            user=admin.user
            admin.delete()
            user.delete()
            messages.success(request,"User Deleted Successfully!")
    return redirect('admin_users')

#not fully done need to design
def signup(request):
    page='signup'
    form=CustomUserCreationForm()
    context={'form':form,'page':page}
    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,"user registered successfully")
            login(request,user)
            return redirect('create_admin',pk=user.id)
        else:
            messages.error(request,"Something Went Wrong!")
    return render(request,'users/login_form.html',context)

#checked
@login_required(login_url='login')
def create_admin(request,pk):
    form=AdminUserForm
    context={'form':form}
    if request.method=='POST':
        user=User.objects.get(id=pk)
        name=user.first_name
        gender=request.POST['gender']
        dob=request.POST['dob']
        address=request.POST['address']
        mobile=request.POST['mobile']
        profile_img=request.FILES['profile_img']
        try:
            admin=Profile.objects.create(user=user,name=name,role='admin',roll_no=name,address=address,profile_img=profile_img,dob=dob,gender=gender,mobile=mobile)
            admin.save()
            messages.success(request,"admin Created successfully!")
            return redirect('home')
        except:
            messages.error(request,"Something went wrong")
            return redirect('home')
    return render(request,'users/create_admin.html',context)

#checked
@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request,'User was logged out!')
    return redirect('home')

#checked    
@login_required(login_url='login')
def my_account(request):
    profile=request.user.profile
    context={'profile':profile}
    return render(request,'users/profile.html',context)
