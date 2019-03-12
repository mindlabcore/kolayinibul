from django import forms
import datetime
from datetime import date


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50, label="Username")
    password = forms.CharField(max_length=20, label="Password", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Confirm Password", widget=forms.PasswordInput)
    email = forms.EmailField()
    date_of_birth = forms.DateField(initial=datetime.date.today)

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (dob.year + 18, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('Must be at least 18 years old to register. Please leave this site.')
        return dob

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        email = self.cleaned_data.get("email")
        date_of_birth = self.cleaned_data.get("date_of_birth")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords are not correct! Please try again.")

        values = {
            "username": username,
            "password": password,
            "email": email,
            "date_of_birth": date_of_birth,

        }
        return values


class ResetForm(forms.Form):
    email = forms.CharField(label="Email")

    def clean(self):
        email = self.cleaned_data.get("email")
        values = {
            "email": email
        }
        return values


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label="Password")
    confirm = forms.CharField(max_length=20, label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords are not correct! Please try again.")

        values = {
            "password": password,
        }
        return values


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
