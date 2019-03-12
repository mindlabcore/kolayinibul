from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url

app_name = "blog"

urlpatterns = [
    path('', views.posts, name="stories"),
    path('categories/<int:id>', views.categories, name="categories"),
    path('post/<slug:slug>', views.detail, name="detail"),
    path('add_post/', views.add_post, name="add_post"),
    path('update/<int:id>', views.update_post, name="update"),
    path('delete/<int:id>', views.delete_post, name="delete"),

]