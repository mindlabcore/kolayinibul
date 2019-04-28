from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from blog.forms import PostForm
from django.contrib import messages
from blog.models import Category, SubCategory, Post
from job.models import JobAdvertisement
from user.models import Profile
from django.views.generic import UpdateView, CreateView, FormView
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.template.loader import render_to_string
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from social_django.models import UserSocialAuth


# Create your views here.
def index(request):
    posts = Post.objects.filter(active_post="2").order_by('-created_date').filter(page_header_content=4)
    context = {
        "posts": posts,
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "help_pages/about_us.html")


def privacy_page(request):
    return render(request, "help_pages/privacy_page.html")


def faq(request):
    return render(request, "help_pages/faq.html")


@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    context = {
        "posts": posts
    }
    return render(request, "profile_pages/dashboard.html", context)


@login_required
def my_posts(request):
    """
    user = request.user
    if not user.is_authenticated:
        products = []  # if olumsuz olarak kullanıldı. (kullanıcı authanticated değilse...)
    else:
        products = Product.objects.filter(seller=request.user)
    """
    posts = Post.objects.filter(author=request.user)
    #  posts = get_object_or_404(Post, author=request.user)
    context = {
        "posts": posts
    }

    return render(request, "profile_pages/my_posts.html", context)


@login_required
def my_profile(request):
    #  detail = Profile.objects.filter(id=id)
    #  profile_detail = Profile.objects.filter(slug=slug)
    profile_detail = get_object_or_404(Profile, user=request.user)
    user_posts = Post.objects.filter(author=profile_detail.id)
    user_jobs = JobAdvertisement.objects.filter(employer=profile_detail.id)


    # GitHub Settings:
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    context = {
        "profile_detail": profile_detail,
        "user_posts": user_posts,
        "user_jobs": user_jobs,
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    }

    return render(request, "profile_pages/my_profile.html", context)


@login_required
def my_jobs(request):
    """
    user = request.user
    if not user.is_authenticated:
        products = []  # if olumsuz olarak kullanıldı. (kullanıcı authanticated değilse...)
    else:
        products = Product.objects.filter(seller=request.user)
    """
    jobs = JobAdvertisement.objects.filter(employer=request.user)
    #  posts = get_object_or_404(Post, author=request.user)
    context = {
        "jobs": jobs
    }

    return render(request, "profile_pages/my_jobs.html", context)


def search_view(request):
    context = {}
    if request.method == "GET":
        search_key = request.GET.get("s")
        print(search_key)
        if search_key:
            context["searching_posts"] = Post.objects.filter(active_post="2").filter(
                Q(title__icontains=search_key) | Q(description__icontains=search_key) |
                Q(author__profile__slug__icontains=search_key) | Q(tag__sub_category__slug__icontains=search_key)

            )

    return render(request, "help_pages/search.html", context)


def job_page_coming_soon(request):
    return render(request, "job_pages/jobs_listing.html")


def categories(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return context


def footerpost(request):
    footer_post = Post.objects.filter(active_post="2").order_by('-created_date')
    context = {
        "footer_post": footer_post,
    }
    return context


def big_box(request):
    try:
        big_box = Post.objects.get(page_header_content=1)

    except Post.DoesNotExist:
        big_box = None
    context = {
        "big_box": big_box,
    }
    return context


def second_box(request):
    try:
        second_box = Post.objects.get(page_header_content=2)

    except Post.DoesNotExist:
        second_box = None
    context = {
        "second_box": second_box,
    }
    return context


def third_box(request):
    try:
        third_box = Post.objects.get(page_header_content=3)

    except Post.DoesNotExist:
        third_box = None
    context = {
        "third_box": third_box,
    }
    return context


def contact_us(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + " Gönderen:" + from_email
            try:
                send_mail(subject, message, 'iletisim@kolayinibul.com', ['iletisim@kolayinibul.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, "Bizimle iletişime geçtiğiniz için teşekkür ederiz!")
            return redirect('index')
    return render(request, "help_pages/contact_us.html", {'form': form})


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def ads(request):
    return render(request, "base/ads/ads")


