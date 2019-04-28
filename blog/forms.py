from django import forms
from .models import Post, Category, SubCategory
from django.forms.models import modelformset_factory


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [

            "category", "sub_category", "title", "description", "image", "sources", "tag"

        ]


class PostForm2(forms.ModelForm):
    class Meta:
        model = Post

        fields = [

            "category", "sub_category", "title", "description", "sources", "image", "tag"

        ]


class ColorfulContactForm(forms.Form):
    class Meta:
        model = Post
        fields = ('category', 'subcategory', 'description',)

    def __init__(self, *args, **kwargs):
        super(ColorfulContactForm, self).__init__(*args, **kwargs)
