from django.db import models
from django.contrib.auth.models import User

# -----------------------
# Employer Model
# -----------------------
class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    website = models.URLField(blank=True)  # Optional company website
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

# -----------------------
# Job Seeker Model
# -----------------------
class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# -----------------------
# Job Model
# -----------------------
class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# -----------------------
# Job Application Model
# -----------------------
class Application(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected')
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.user.username} - {self.job.title}"

# -----------------------
# Interview Model
# -----------------------
class Interview(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]
    MODE_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline')
    ]

    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    interview_date = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='Online')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.candidate.user.username} - {self.interview_date.strftime('%Y-%m-%d %H:%M')}"
