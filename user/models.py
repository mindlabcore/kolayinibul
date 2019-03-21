from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import Post, Category, SubCategory
from django.contrib.auth.models import AbstractUser


class UsersPosts(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ownpost')
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ownpost')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=55, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    job = models.CharField(max_length=30, blank=True)
    skills = models.ManyToManyField(SubCategory)
    post = models.ManyToManyField(Post, blank=True)
    followers = models.ManyToManyField(User, blank=True, verbose_name="Followers", related_name="Followers")
    following = models.ManyToManyField(User, blank=True, verbose_name="Following", related_name="Following")

    def save(self, *args, **kwargs):
        print(self.user.username)

        if not self.slug:
            self.slug = self.get_slug()
            print(self.slug)
        print(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return "{username}".format(username=self.user.username)

    def get_slug(self):
        slug = self.user.username.replace("ı", "i")
        return slugify(slug)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
