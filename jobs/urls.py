from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/jobseeker/', views.register_jobseeker, name='register_jobseeker'),
    path('register/employer/', views.register_employer, name='register_employer'),
    path('post-job/', views.post_job, name='post_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    
    # Job Seeker URLs
    path('applications/', views.my_applications, name='my_applications'),
    path('my-applications/', views.my_applications, name='my_applications'),

    # Employer URLs for managing applications
    path('applications/<int:job_id>/', views.applications_list, name='applications_list'),
    path('applications/update/<int:app_id>/', views.update_application, name='update_application'),
    path('interviews/schedule/<int:app_id>/', views.schedule_interview, name='schedule_interview'),
]
