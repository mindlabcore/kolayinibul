from django.contrib import admin
from .models import JobAdvertisement


@admin.register(JobAdvertisement)
class JobAdvertisementAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "title", "sub_category", "employer", "created_date", "job_status"]

    class Meta:
        model = JobAdvertisement
