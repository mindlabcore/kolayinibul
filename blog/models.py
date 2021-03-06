from django.db import models
from django.db import models
from django.db.models import F
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name="Category Adı")
    slug = models.SlugField(max_length=55, blank=True, null=True)

    def save(self, *args, **kwargs):
        print(self.category_name)

        if not self.slug:
            self.slug = self.get_slug()
            print(self.slug)
        print(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return "{category_name}".format(category_name=self.category_name)

    def get_slug(self):
        slug = self.category_name.replace("ı", "i")
        return slugify(slug)

    def get_absolute_url(self):
        return reverse('categories:categories', args=[str(self.slug)])


class SubCategory(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='subcategories')
    sub_category_name = models.CharField(max_length=50, verbose_name="Alt-Category Adı")
    slug = models.SlugField(max_length=55, blank=True, null=True)
    sub_category_image = models.FileField(upload_to='sub_category_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        print(self.sub_category_name)

        if not self.slug:
            self.slug = self.get_slug()
            print(self.slug)
        print(self.sub_category_name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return "{sub_category_name}".format(sub_category_name=self.sub_category_name)

    def get_slug(self):
        slug = self.sub_category_name.replace("ı", "i")
        return slugify(slug)

    def get_absolute_url(self):
        return reverse('categories:subcategories', args=[str(self.slug)])


class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Yazar")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Kategori Adı")
    sub_category = models.ForeignKey("SubCategory", on_delete=models.CASCADE, verbose_name="Alt Kategori Adı",
                                     related_name="sub_category")
    title = models.CharField(max_length=50, verbose_name="Post Başlığı")
    slug = models.SlugField(max_length=55, blank=True, null=True)
    description = RichTextField(max_length=100000, null=False, verbose_name="Açıklama")
    image = models.ImageField(upload_to='post_images/', null=True, blank=True,
                              default='')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_date = models.DateTimeField(blank=True, null=True, verbose_name="Updated Date")
    verified_date = models.DateTimeField(auto_now_add=True, verbose_name="Verified Date")
    sources = models.CharField(max_length=250, verbose_name="Kaynak", blank=True, null=True)

    STATUS_DRAFT = 1
    STATUS_PUBLISHED = 2
    STATUS_ARCHIVED = 3
    STATUS_DEACTIVATED = 4
    STATUS_WAITING_APPROVAL = 5
    STATUSES = (
        (STATUS_DRAFT, 'Taslak'),
        (STATUS_PUBLISHED, 'Yayında'),
        (STATUS_ARCHIVED, 'Arşivlendi'),
        (STATUS_DEACTIVATED, 'Kaldırıldı'),
        (STATUS_WAITING_APPROVAL, "Onay Bekliyor")
    )
    active_post = models.SmallIntegerField(choices=STATUSES, default=5)
    #  Page Header Content'de bir büyük iki küçük box'ta görünmesi için üç değer verelim.
    LOCATION_BIG = 1
    LOCATION_SMALL1 = 2
    LOCATION_SMALL2 = 3
    LOCATION_OTHER = 4
    LOCATION = (
        (LOCATION_BIG, 'Big Box'),
        (LOCATION_SMALL1, 'First Small Box'),
        (LOCATION_SMALL2, 'Second Small Box'),
        (LOCATION_OTHER, 'Other'),
    )
    page_header_content = models.SmallIntegerField(choices=LOCATION, default=4)
    tag = models.ManyToManyField(SubCategory, default=sub_category)

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

    def get_absolute_url(self):
        return reverse('posts:detail', args=[str(self.slug)])

    class Meta:
        ordering = ['-created_date']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Post", related_name="comments")
    comment_author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Yorum Sahibi")
    comment_content = models.CharField(max_length=1000, verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['comment_date']
