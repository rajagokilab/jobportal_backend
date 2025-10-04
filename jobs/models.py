from django.db import models
from django.contrib.auth.models import User

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.user.username

class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[('Applied','Applied'), ('Shortlisted','Shortlisted'), ('Rejected','Rejected')],
        default='Applied'
    )

    def __str__(self):
        return f"{self.candidate.user.username} - {self.job.title}"

class Interview(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    interview_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('Scheduled','Scheduled'),('Completed','Completed')])

    def __str__(self):
        return f"{self.application.candidate.user.username} - {self.interview_date}"
