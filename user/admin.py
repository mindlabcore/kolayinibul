from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Profile, Avatar


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "job"]
    list_display_links = ["id", "user", "job"]

    class Meta:
        model = Profile
