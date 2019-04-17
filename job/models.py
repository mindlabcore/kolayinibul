from django.db import models
from django.db.models import F
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from blog.models import Category, SubCategory


class JobAdvertisement(models.Model):
    employer = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="İşveren")
    company_name = models.CharField(max_length=50, verbose_name="Firma Adı", blank=True, null=True)
    email_adress = models.EmailField(blank=True, null=True)
    avg_salary = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name="Ortalama Maaş")
    category = models.ForeignKey('blog.Category', on_delete=models.CASCADE, verbose_name="Kategori Adı",
                                 related_name="job_category")
    sub_category = models.ForeignKey('blog.SubCategory', on_delete=models.CASCADE, verbose_name="Alt Kategori Adı",
                                     related_name="job_sub_category")
    title = models.CharField(max_length=50, verbose_name="Pozisyon")
    slug = models.SlugField(max_length=55, blank=True, null=True)
    description = RichTextField(max_length=100000, null=False, verbose_name="İş Açıklaması")
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True,
                                     default='')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_date = models.DateTimeField(blank=True, null=True, verbose_name="Updated Date")
    verified_date = models.DateTimeField(auto_now_add=True, verbose_name="Verified Date")

    TYPE_COMPANY = 1
    TYPE_INDIVIDUAL = 2
    TYPES = (
        (TYPE_COMPANY, 'Firma'),
        (TYPE_INDIVIDUAL, 'Bireysel')
    )
    type = models.SmallIntegerField(choices=TYPES, verbose_name="İşveren Tipi")

    TERM_SHORT = 1
    TERM_LONG = 2
    TERM_ONE_TIME = 3
    TERM_INTERNSHIP = 4
    TERM_REMOTE = 5
    TERMS = (
        (TERM_SHORT, 'Kısa Dönem'),
        (TERM_LONG, 'Uzun Dönem'),
        (TERM_ONE_TIME, 'Tek Seferlik'),
        (TERM_INTERNSHIP, 'Staj'),
        (TERM_REMOTE, 'Remote')
    )
    term = models.SmallIntegerField(choices=TERMS, verbose_name="Dönem")

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
    job_status = models.SmallIntegerField(choices=STATUSES, default=5)
    tag = models.ManyToManyField(SubCategory, default=sub_category)

    def save(self, *args, **kwargs):
        print(self.title)

        if not self.slug:
            self.slug = self.get_slug()
            print(self.slug)
        print(self.title)
        super(JobAdvertisement, self).save(*args, **kwargs)

    def __str__(self):
        return "{title} - {pk} - {company_name}".format(pk=self.pk, title=self.title, company_name=self.company_name)

    def get_slug(self):
        slug = self.title.replace("ı", "i")
        slug += "-" + get_random_string(4)
        return slugify(slug)

    def get_absolute_url(self):
        return reverse('jobs:detail', args=[str(self.slug)])
