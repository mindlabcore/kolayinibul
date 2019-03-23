from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [

            "category", "sub_category", "title", "description", "tag"

        ]
