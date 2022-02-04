from django.urls import path
from . import views

urlpatterns=[
    
    path('subject',views.subject,name='subject'),
    path('create_subject',views.create_subject,name='create_subject'),
    path('update_subject/<str:pk>',views.update_subject,name='update_subject'),
    path('semester',views.semester,name='semester'),
    path('view_result/<str:pk>',views.results,name='results'),
    path('my_results',views.my_results,name='my_results'),
    
    path('create_sem',views.create_sem,name='create_sem'),
    path('update_sem/<str:pk>',views.update_sem,name='update_sem'),

    path('students_result_home',views.students_result_home,name='student_result_home'),
    path('students_result',views.students_result,name='students_result'),
    path('admin_result_view/<str:pk>',views.admin_result_view,name='admin_result_view'),
    path('create_result/<str:pk>',views.create_result,name='create_result'),
    path('update_result_view/<str:pk>',views.update_result_view,name='update_result_view'),
    path('csv_upload',views.csv_upload,name='csv_upload'),

    path('dept_sem_papers',views.dept_sem_papers,name='dept_sem_papers'),
    path('create_dept_sem_papers',views.create_dept_sem_papers,name='create_dept_sem_papers'),
    path('update_dept_sem_papers/<str:pk>',views.update_dept_sem_papers,name='update_dept_sem_papers'),

    path('update_result/<str:pk>',views.update_result,name='update_result'),
    path('delete_result/<str:pk>',views.delete_result,name='delete_result')
    
    ]
    