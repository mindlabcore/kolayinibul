from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "job"]
    list_display_links = ["id", "user", "job"]
    filter_horizontal = ('post',)

    #  filter horizontal'ı araştır. Tam buraya m2m ile koyabilirsin.

    class Meta:
        model = Profile
