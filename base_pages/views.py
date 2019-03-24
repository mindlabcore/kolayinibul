from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from blog.forms import PostForm
from django.contrib import messages
from blog.models import Category, SubCategory, Post
from django.views.generic import UpdateView, CreateView, FormView
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.
def index(request):
    posts = Post.objects.filter(active_post="2").order_by('-created_date')
    context = {
        "posts": posts,
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "help_pages/about_us.html")


def faq(request):
    return render(request, "help_pages/faq.html")


def contact_us(request):
    return render(request, "help_pages/contact_us.html")


@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    context = {
        "posts": posts
    }
    return render(request, "profile_pages/dashboard.html", context)


@login_required
def my_profile(request):
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

    return render(request, "profile_pages/my_profile.html", context)


def search_view(request):
    context = {}
    if request.method == "GET":
        search_key = request.GET.get("s")
        print(search_key)
        if search_key:
            context["searching_posts"] = Post.objects.filter(active_post="2").filter(
                Q(title__icontains=search_key) | Q(description__icontains=search_key)

            )

    return render(request, "help_pages/search.html", context)


def job_page_coming_soon(request):
    return render(request, "job_pages/coming_soon.html")


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
