from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import PostForm
from django.contrib import messages
from .models import Post, Category, SubCategory
from django.contrib.auth.decorators import login_required


def categories(request, id):
    # categories = get_object_or_404(Product,id = id)
    posts = Post.objects.filter(active_post=True).filter(category=id)
    context = {
        "posts": posts,

    }
    return render(request, "category_pages/categories_detail.html", context)


def posts(request):
    posts = Post.objects.all()
    context = {
        "posts": posts
    }
    return render(request, context)


@login_required
def detail(request, slug):
    # story = Story.objects.filter(id = id).first()
    post = get_object_or_404(Post, slug=slug)
    # story = Story.objects.filter(slug=slug)
    return render(request, "post_pages/detail_post.html", {"post": post})


@login_required
def add_post(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        story = form.save(commit=False)
        story.author = request.user
        story.save()
        messages.success(request, "Post created successful!")
        return redirect("index")

    return render(request, "post_pages/new_post.html", {"form": form})


@login_required
def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Post changed successful!")
        return redirect("post:dashboard")

    return render(request, "post_pages/update_post.html", {"form": form})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    post.delete()

    messages.success(request, "Post deleted successful!")

    return redirect("post:dashboard")
