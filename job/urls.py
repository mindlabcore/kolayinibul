from django.urls import path
from . import views

app_name = "job"

urlpatterns = [
    path('', views.jobs, name="jobs"),
    path('job/<slug:slug>', views.detail, name="detail"),
    path('add_job/', views.add_job, name="add_post"),
    path('update/<slug:slug>', views.update_job, name="update"),
    path('delete/<slug:slug>', views.delete_job, name="delete"),
    path('1', views.listing, name="listing"),

]

