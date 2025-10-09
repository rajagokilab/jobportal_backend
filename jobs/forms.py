from django import forms
from django.contrib.auth.models import User
from .models import JobSeeker, Employer, Job, Application, Interview

# -----------------------
# User Registration Form
# -----------------------
class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Password confirmation validation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

# -----------------------
# Job Seeker Form
# -----------------------
class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['resume']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'})
        }

# -----------------------
# Employer Form
# -----------------------
class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'website']

# -----------------------
# Job Posting Form
# -----------------------
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }

# -----------------------
# Application Status Update Form
# -----------------------
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']

# -----------------------
# Interview Scheduling Form
# -----------------------
class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interview_date', 'status', 'location', 'mode']
        widgets = {
            'interview_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# -----------------------
# Login Form
# -----------------------
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
