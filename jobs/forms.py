from django import forms
from django.contrib.auth.models import User
from .models import JobSeeker, Employer, Job, Application, Interview

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['resume']

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interview_date', 'status']
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
