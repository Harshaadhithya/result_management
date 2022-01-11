from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('profile',views.profile,name='profile'),

    path('dept',views.dept,name='dept'),
    path('create_department/',views.create_dept,name='create_department'),


    path('update_department/<str:pk>',views.update_department,name='update_department'),
    path('create_student/',views.create_student,name='create_student'),
    

    path('user-login/',views.user_login,name='login'),
    path('signup/',views.signup,name='signup'),

    path('my_account',views.my_account,name='my_account'),


    path('user-logout/',views.logout_user,name='logout'),
    path('create_admin/<str:pk>',views.create_admin,name='create_admin'),
    path('delete_admin/<str:pk>',views.delete_admin,name='delete_admin'),

    path('students',views.students,name='students'),
    path('student_profile/<str:pk>',views.student_profile,name='student_profile'),
    path('create_user',views.create_student,name='create_user'),
    path('edit_student/<str:pk>',views.edit_student_by_admin,name='edit_student'),

    path('admin_users',views.admin_users,name='admin_users'),
    path('verify_admin/<str:pk>',views.verify_admin,name='verify_admin')

]
