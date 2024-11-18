from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.core.exceptions import ValidationError
from .models import ProfileModel
import re

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise ValidationError("Password harus minimal 8 karakter")
        
        if not re.search("[A-Z]", password):
            raise ValidationError("Password harus mengandung setidaknya satu huruf besar")
        if not re.search("[a-z]", password):
            raise ValidationError("Password harus mengandung setidaknya satu huruf kecil.")
        if not re.search("[0-9]", password):
            raise ValidationError("Password harus mengandung setidaknya satu angka.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Password tidak cocok")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'})
        }

class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.ClearableFileInput(attrs=
        {'class': 'form-control form-control-sm'})
    )
    class Meta:
        model = ProfileModel
        fields = ['avatar']

