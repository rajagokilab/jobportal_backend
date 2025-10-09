from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Registration
    path('register/jobseeker/', views.register_jobseeker, name='register_jobseeker'),
    path('register/employer/', views.register_employer, name='register_employer'),

    # Job Posting
    path('post-job/', views.post_job, name='post_job'),

    # Job Applications
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('applications/', views.my_applications, name='my_applications'),

    # Employer Application Management
    path('applications/<int:job_id>/list/', views.applications_list, name='applications_list'),
    path('applications/update/<int:app_id>/', views.update_application, name='update_application'),
    path('interviews/schedule/<int:app_id>/', views.schedule_interview, name='schedule_interview'),
]
