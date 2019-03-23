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
        "posts": posts,
    }
    return render(request, context)


@login_required
def detail(request, slug):
    # story = Story.objects.filter(id = id).first()
    post = get_object_or_404(Post, slug=slug)
    tag = post.tag.all()
    # story = Story.objects.filter(slug=slug)
    context = {
        "post": post,
        "tag": tag,

    }
    return render(request, "post_pages/detail_post.html", context)


@login_required
def add_post(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        story = form.save(commit=False)
        story.author = request.user
        story.save()
        messages.success(request, "Post başarıyla oluşturuldu!")
        return redirect("my_profile")

    return render(request, "post_pages/new_post.html", {"form": form})


@login_required
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if post.author != request.user:
        messages.error(request, "Bu işlem için yetkili değilsiniz!")
        return redirect("posts:detail", slug=post.slug)

    else:
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post changed successful!")
            return redirect("posts:detail", slug=post.slug)
        context = {
            "post": post,
            "form": form,
        }
    return render(request, "post_pages/update_post.html", context)


@login_required
def delete_post(request, slug):
    #  Silmek yerine passive yapsak daha iyi olur.
    post = get_object_or_404(Post, slug=slug)
    #  post.delete()
    if post.author == request.user:
        if post.active_post == True:
            post.active_post = False
        else:
            post.active_post = True
            post.save()
            messages.success(request, "Post yayından kaldırıldı!")
    else:
        messages.error(request, "Bu işlem için yetkili değilsiniz!")
    return redirect("posts:detail", slug=post.slug)
