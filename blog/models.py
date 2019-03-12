from django.db import models
from django.db import models
from django.db.models import F
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name="Category Name")

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    sub_category_name = models.CharField(max_length=50, verbose_name="Sub-Category Name")

    def __str__(self):
        return self.sub_category_name


class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Author")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Category Name")
    sub_category = models.ForeignKey("SubCategory", on_delete=models.CASCADE, verbose_name="Sub-Category Name",
                                     related_name="sub_category")
    title = models.CharField(max_length=50, verbose_name="Story Title")
    slug = models.SlugField(max_length=55, blank=True, null=True)
    description = RichTextField(max_length=100000, null=False)
    image = models.ImageField(upload_to='story_images/', null=True, blank=True,
                              default='')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    verified_date = models.DateTimeField(auto_now_add=True, verbose_name="Verified Date")
    active_post = models.BooleanField(default=True)
    tag = models.ManyToManyField(SubCategory)

    def __str__(self):
        return "{title} - {pk}".format(pk=self.pk, title=self.title)

    def get_slug(self):
        slug = self.title.replace("ı", "i")
        slug += "-" + get_random_string(4)
        return slugify(slug)
