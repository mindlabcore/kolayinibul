from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "user"

urlpatterns = [
    path('sign_up/', views.sign_up, name="sign_up"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('reset_password/', views.send_reset_link, name="reset_password"),
    path('create_new_password/', views.create_new_password, name="create_new_password"),
    path('profile/<slug:slug>/', views.profile, name="profile"),


]
