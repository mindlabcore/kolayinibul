from django import forms
from .models import JobAdvertisement
from blog.models import Category, SubCategory, Post
from blog.forms import PostForm
from blog import models


class JobAdvertisementForm(forms.ModelForm):
    class Meta:
        model = JobAdvertisement

        fields = [

            "category", "sub_category", "title", "description", "type", "term", "company_name", "tag",
            "company_logo"

        ]
