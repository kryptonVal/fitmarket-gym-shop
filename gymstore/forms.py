from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# User registration form
class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already registered')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already registered')
        return username

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise ValidationError('Passwords do not match')
        return confirm_password
