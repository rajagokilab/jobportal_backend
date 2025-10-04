from django.contrib import admin
from .models import Employer, JobSeeker, Job, Interview

admin.site.register([Employer, JobSeeker, Job, Interview])
