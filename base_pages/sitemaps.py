from django.contrib.sitemaps import Sitemap
from blog.models import Post, Category, SubCategory
from django.urls import reverse
from job.models import JobAdvertisement


class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = "0.8"

    def items(self):
        return Post.objects.filter(active_post=2)


class CategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = "0.8"

    def items(self):
        return Category.objects.filter()


class SubcategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = "0.6"

    def items(self):
        return SubCategory.objects.filter()


class JobAdvertisementSitemap(Sitemap):
    changefreq = 'weekly'
    priority = "0.6"

    def items(self):
        return JobAdvertisement.objects.all()


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = "1"

    def items(self):
        return ['index', 'about_us', 'contact_us', 'privacy_page']

    def location(self, item):
        return reverse(item)
