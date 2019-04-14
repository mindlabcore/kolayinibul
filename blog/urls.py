from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)
from base_pages import views as base_pages_views

app_name = "blog"

urlpatterns = [
    path('', views.posts, name="posts"),
    path('<slug:slug>', views.categories, name="categories"),
    path('subcategories/<slug:slug>', views.sub_categories, name="subcategories"),
    path('post/<slug:slug>', views.detail, name="detail"),
    path('add_post/', views.add_post, name="add_post"),
    path('update/<slug:slug>', views.update_post, name="update"),
    path('delete/<slug:slug>', views.delete_post, name="delete"),

]

