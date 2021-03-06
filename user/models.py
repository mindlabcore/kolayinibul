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
from django.utils.translation import ugettext_lazy as _


class UsersPosts(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ownpost')
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ownpost')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=55, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biyografi")
    school = models.CharField(max_length=30, blank=True, verbose_name="Okul")
    education = models.CharField(max_length=30, blank=True, verbose_name="Bölüm")
    city = models.CharField(max_length=30, blank=True, verbose_name="Şehir")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Doğum Tarihi")
    avatar = models.ImageField(upload_to='avatars/', default='avatars/defaultuser.jpg', verbose_name="Profil Fotoğrafı")
    job = models.CharField(max_length=30, blank=True, verbose_name="Meslek")
    skills = models.ManyToManyField(SubCategory, verbose_name="Yetenekler")
    post = models.ManyToManyField(Post, blank=True)
    followers = models.ManyToManyField(User, blank=True, verbose_name="Followers", related_name="Followers")
    following = models.ManyToManyField(User, blank=True, verbose_name="Following", related_name="Following")
    github_profile = models.URLField(verbose_name="Github Profile", null=True, blank=True)
    twitter_profile = models.URLField(verbose_name="Twitter Profile", null=True, blank=True)
    stack_overflow_profile = models.URLField(verbose_name="Stack Overflow Profile", null=True, blank=True)
    facebook_profile = models.URLField(verbose_name="Facebook Profile", null=True, blank=True)
    instagram_profile = models.URLField(verbose_name="Instagram Profile", null=True, blank=True)
    linkedin_profile = models.URLField(verbose_name="Linkedin Profile", null=True, blank=True)
    skype_profile = models.URLField(verbose_name="Skype Profile", null=True, blank=True)
    spotify_profile = models.URLField(verbose_name="Spotify Profile", null=True, blank=True)

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

    def get_full_name(self):
        """ Short cut method that duplicates user.get_full_name """
        return "{} {}".format(self.first_name, self.last_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
