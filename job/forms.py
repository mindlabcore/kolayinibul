from django import forms
from .models import JobAdvertisement
from blog.models import Category, SubCategory, Post
from blog.forms import PostForm
from blog import models
from ckeditor.fields import RichTextField, RichTextFormField


class JobAdvertisementForm(forms.ModelForm):
    class Meta:
        model = JobAdvertisement

        fields = [

            "category", "sub_category", "title", "description", "type", "term", "company_name", "tag", "avg_salary",
            "company_logo"

        ]


class JobAdvertisementForm2(forms.Form):
    category = forms.ModelChoiceField(required=True, label="İş Kategorisi", queryset=Category.objects.all())
    sub_category = forms.ModelChoiceField(required=True, label="Alt Kategori",
                                          queryset=SubCategory.objects.all())
    title = forms.CharField(required=True, label="Başlık")
    description = forms.CharField(label='Açıklama',
                                  widget=forms.Textarea(attrs={'class': 'ckeditor'}), required=True)
    type = forms.ModelChoiceField(required=True, label="İşveren Tipi", queryset=JobAdvertisement.objects.all())
    term = forms.ModelChoiceField(required=True, label="Dönem", queryset=JobAdvertisement.objects.all())
    company_name = forms.CharField(required=True, label="Firma Adı")
    tag = forms.ModelMultipleChoiceField(required=True, label="Tags",
                                         queryset=JobAdvertisement.objects.all())
    company_logo = forms.ImageField(required=True, label="Firma Logosu")
