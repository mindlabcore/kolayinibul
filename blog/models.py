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
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='subcategories')
    sub_category_name = models.CharField(max_length=50, verbose_name="Sub-Category Name")
    sub_category_image = models.FileField(upload_to='sub_category_images/', null=True, blank=True)

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
    updated_date = models.DateTimeField(blank=True, null=True, verbose_name="Updated Date")
    verified_date = models.DateTimeField(auto_now_add=True, verbose_name="Verified Date")

    STATUS_DRAFT = 1
    STATUS_PUBLISHED = 2
    STATUS_ARCHIVED = 3
    STATUS_DEACTIVATED = 4
    STATUSES = (
        (STATUS_DRAFT, 'Taslak'),
        (STATUS_PUBLISHED, 'Yayında'),
        (STATUS_ARCHIVED, 'Arşivlendi'),
        (STATUS_DEACTIVATED, 'Kaldırıldı')
    )
    active_post = models.SmallIntegerField(choices=STATUSES, default="2")
    tag = models.ManyToManyField(SubCategory)

    def save(self, *args, **kwargs):
        print(self.title)

        if not self.slug:
            self.slug = self.get_slug()
            print(self.slug)
        print(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return "{title} - {pk}".format(pk=self.pk, title=self.title)

    def get_slug(self):
        slug = self.title.replace("ı", "i")
        slug += "-" + get_random_string(4)
        return slugify(slug)
