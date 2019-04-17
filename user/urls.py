from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "user"

urlpatterns = [
    path('sign_up/', views.sign_up, name="sign_up"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('change_password/', views.change_password, name="change_password"),
    path('profile/<slug:slug>/', views.profile, name="profile"),
    path('edit_profile/', views.update_profile, name="update_profile"),


]
