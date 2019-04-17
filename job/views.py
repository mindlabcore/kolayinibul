from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import JobAdvertisementForm
from django.contrib import messages
from .models import JobAdvertisement
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def jobs(request):
    jobs = JobAdvertisement.objects.all().order_by('-created_date')

    context = {
        "jobs": jobs,
    }
    return render(request, 'job_pages/jobs_listing.html', context)


def detail(request, slug):
    # story = Story.objects.filter(id = id).first()
    job = get_object_or_404(JobAdvertisement, slug=slug)
    tag = job.tag.all()
    # story = Story.objects.filter(slug=slug)
    context = {
        "job": job,
        "tag": tag,
    }
    return render(request, "job_pages/detail_job.html", context)


@login_required
def add_job(request):
    form = JobAdvertisementForm(request.POST or None, request.FILES or None)


    if form.is_valid():
        job = form.save(commit=False)
        job.employer = request.user
        job.save()
        form.save_m2m()

        messages.success(request,
                         "İş ilanı başarıyla oluşturuldu! Düzenleyebilmen için taslak halinde profilinde seni bekliyor. "
                         "Tek yapman gereken yayına almak!")
        return redirect("my_profile")

    return render(request, "job_pages/new_job.html", {"form": form})


@login_required
def update_job(request, slug):
    #  Profile sayfası.
    job = get_object_or_404(JobAdvertisement, slug=slug)
    form = JobAdvertisementForm(request.POST or None, request.FILES or None, instance=post)
    if job.employer != request.user:
        messages.error(request, "Bu işlem için yetkili değilsiniz!")
        return redirect("jobs:detail", slug=job.slug)

    else:
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.updated_date = timezone.now()
            job.save()
            form.save_m2m()

            messages.success(request, "İş ilanı başarıyla değiştirildi!")
            return redirect("jobs:detail", slug=job.slug)
        context = {
            "job": job,
            "form": form,
        }
    return render(request, "job_pages/update_job.html", context)


@login_required
def delete_job(request, slug):
    #  Silmek yerine passive yapsak daha iyi olur. Profile sayfası.
    job = get_object_or_404(JobAdvertisement, slug=slug)
    #  post.delete()
    if job.employer == request.user:
        if job.job_status == 2:
            job.job_status = 4
            job.save()
            messages.success(request, "İş ilanı yayından kaldırıldı!")
        else:
            job.active_post = 2
            job.save()
            messages.success(request, "İş ilanı yayına alındı!")
    else:
        messages.error(request, "Bu işlem için yetkili değilsiniz!")
        return redirect("jobs:detail", slug=job.slug)
    return redirect("my_profile")


def listing(request):

    return render(request, 'job_pages/joblist_theme.html')