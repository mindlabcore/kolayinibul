"""kolayinibul URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog import views as post_views
from base_pages import views as base_pages_view
from blog import views as blog_views
from job import views as job_views
from django.conf import settings
from django.conf.urls.static import static
from base_pages.sitemaps import PostSitemap, StaticViewSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'posts': PostSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    # admin App:
    path('admin/', admin.site.urls),

    # user App:
    path('user/', include("user.urls", namespace="user")),
    path('accounts/login', include('django.contrib.auth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('django.contrib.auth.urls')),

    # blog App:
    path('posts/', include("blog.urls", namespace="posts")),
    path('categories/', include("blog.urls", namespace="categories")),
    path('categories/<slug:slug>', blog_views.categories, name="categories"),

    # job App:
    path('jobs/', include("job.urls", namespace="jobs")),


    # base_pages App:
    path('', base_pages_view.index, name="index"),
    path('about_us/', base_pages_view.about, name="about_us"),
    path('dashboard/', base_pages_view.dashboard, name="dashboard"),
    path('my_posts/', base_pages_view.my_posts, name="my_posts"),
    path('my_jobs/', base_pages_view.my_jobs, name="my_jobs"),
    path('my_profile/', base_pages_view.my_profile, name="my_profile"),
    path('faq/', base_pages_view.faq, name="faq"),
    path('contact_us/', base_pages_view.contact_us, name="contact_us"),
    path('search/', base_pages_view.search_view, name="search_view"),
    path('privacy_page/', base_pages_view.privacy_page, name="privacy_page"),
    path('jobs/', base_pages_view.job_page_coming_soon, name="job_page_coming_soon"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    # Advertorials
    path('ads.txt/', base_pages_view.ads, name="ads"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
