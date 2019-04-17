from django.contrib.sitemaps import Sitemap
from blog.models import Post
from django.urls import reverse
from job.models import JobAdvertisement


class PostSitemap(Sitemap):

    def items(self):
        return Post.objects.all()


class JobAdvertisementSitemap(Sitemap):

    def items(self):
        return JobAdvertisement.objects.all()


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['about_us']

    def location(self, item):
        return reverse(item)


