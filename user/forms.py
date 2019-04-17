from django import forms
import datetime
from datetime import date
from user.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50, label="Kullanıcı Adı")
    password = forms.CharField(max_length=20, label="Şifre", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Şifre Onayla", widget=forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, label="İsim")
    last_name = forms.CharField(max_length=150, label="Soyisim")

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        email = self.cleaned_data.get("email")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar birbiriyle uyuşmuyor!")

        values = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,

        }
        return values


#  with e-mail
class ChangePasswordForm(forms.Form):
    password = forms.CharField(label="Password")
    confirm = forms.CharField(max_length=20, label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar birbiriyle uyuşmuyor!")

        values = {
            "password": password,
        }
        return values


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = [

            "first_name",
            "last_name",
            "bio",
            "school",
            "education",
            "city",
            "birth_date",
            "avatar",
            "job",
            "skills",
            "github_profile",
            "twitter_profile",
            "stack_overflow_profile",
            "facebook_profile",
            "instagram_profile",
            "linkedin_profile",
            "skype_profile",
            "spotify_profile"

        ]
