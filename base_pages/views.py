from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from blog.forms import PostForm
from django.contrib import messages
from blog.models import Category, SubCategory, Post
from django.views.generic import UpdateView, CreateView, FormView
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.template.loader import render_to_string
from .forms import ContactForm


# Create your views here.
def index(request):
    posts = Post.objects.filter(active_post="2").order_by('-created_date').filter(page_header_content=4)
    context = {
        "posts": posts,
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "help_pages/about_us.html")


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
                Q(title__icontains=search_key) | Q(description__icontains=search_key) |
                Q(author__profile__slug__icontains=search_key) | Q(tag__sub_category__slug__icontains=search_key)

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
    return render(request, 'help_pages/404.html', status=404)


def handler500(request):
    return render(request, 'help_pages/500.html', status=500)
