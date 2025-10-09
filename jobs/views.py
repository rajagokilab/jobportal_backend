from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, JobSeeker, Employer, Application, Interview
from .forms import (
    UserForm, JobSeekerForm, EmployerForm, JobForm,
    ApplicationForm, InterviewForm, LoginForm
)

# ========================
# Public Views
# ========================
def home(request):
    jobs = Job.objects.all()
    return render(request, 'home.html', {'jobs': jobs})

# ------------------------
# Registration Views
# ------------------------
def register_jobseeker(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        seeker_form = JobSeekerForm(request.POST, request.FILES)
        if user_form.is_valid() and seeker_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            seeker = seeker_form.save(commit=False)
            seeker.user = user
            seeker.save()
            login(request, user)
            messages.success(request, "Job Seeker registered successfully.")
            return redirect('home')
    else:
        user_form = UserForm()
        seeker_form = JobSeekerForm()
    return render(request, 'register_jobseeker.html', {'user_form': user_form, 'seeker_form': seeker_form})

def register_employer(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        employer_form = EmployerForm(request.POST)
        if user_form.is_valid() and employer_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            employer = employer_form.save(commit=False)
            employer.user = user
            employer.save()
            login(request, user)
            messages.success(request, "Employer registered successfully.")
            return redirect('home')
    else:
        user_form = UserForm()
        employer_form = EmployerForm()
    return render(request, 'register_employer.html', {'user_form': user_form, 'employer_form': employer_form})

# ------------------------
# Authentication Views
# ------------------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                messages.success(request, f"Welcome {user.username}!")
                return redirect(next_url)
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

# ========================
# Job Views
# ========================
@login_required
def post_job(request):
    if not hasattr(request.user, 'employer'):
        messages.error(request, "Only employers can post jobs.")
        return redirect('home')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user.employer
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect('home')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if not hasattr(request.user, 'jobseeker'):
        messages.error(request, "Only job seekers can apply.")
        return redirect('home')
    seeker = request.user.jobseeker
    application, created = Application.objects.get_or_create(job=job, candidate=seeker)
    if created:
        messages.success(request, f"Applied for {job.title} successfully.")
    else:
        messages.info(request, f"You have already applied for {job.title}.")
    return render(request, 'apply_job.html', {'job': job, 'application': application, 'created': created})

# ========================
# Job Seeker Views
# ========================
@login_required
def my_applications(request):
    if not hasattr(request.user, 'jobseeker'):
        messages.error(request, "Access denied.")
        return redirect('home')
    seeker = request.user.jobseeker
    applications = Application.objects.filter(candidate=seeker)
    return render(request, 'my_applications.html', {'applications': applications})

# ========================
# Employer Views
# ========================
@login_required
def applications_list(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if not hasattr(request.user, 'employer') or job.employer != request.user.employer:
        messages.error(request, "Access denied.")
        return redirect('home')
    applications = Application.objects.filter(job=job)
    return render(request, 'applications_list.html', {'job': job, 'applications': applications})

@login_required
def update_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    if not hasattr(request.user, 'employer') or application.job.employer != request.user.employer:
        messages.error(request, "Access denied.")
        return redirect('home')
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, f"Application status updated for {application.candidate.user.username}.")
            return redirect('applications_list', job_id=application.job.id)
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'update_application.html', {'form': form, 'application': application})

@login_required
def schedule_interview(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    if not hasattr(request.user, 'employer') or application.job.employer != request.user.employer:
        messages.error(request, "Access denied.")
        return redirect('home')
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            messages.success(request, f"Interview scheduled for {application.candidate.user.username}.")
            return redirect('applications_list', job_id=application.job.id)
    else:
        form = InterviewForm()
    return render(request, 'schedule_interview.html', {'form': form, 'application': application})
