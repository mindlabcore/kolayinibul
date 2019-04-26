from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import PostForm
from django.contrib import messages
from .models import Post, Category, SubCategory, Comment
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def sub_categories(request, slug):
    subcategory_list = Post.objects.filter(active_post="2").filter(sub_category__slug=slug)

    context = {
        "subcategory_list": subcategory_list,
    }
    return render(request, "category_pages/subcategories_detail.html", context)


def categories(request, slug):
    category_list = Post.objects.filter(active_post="2").filter(category__slug=slug)

    context = {
        "category_list": category_list,
    }
    return render(request, "category_pages/categories_detail.html", context)


def posts(request):
    posts = Post.objects.all().order_by('-created_date')

    context = {
        "posts": posts,
    }
    return render(request, context)


def detail(request, slug):
    # story = Story.objects.filter(id = id).first()
    post = get_object_or_404(Post, slug=slug)
    tag = post.tag.all()
    # story = Story.objects.filter(slug=slug)
    comment = post.comments.all()
    context = {
        "post": post,
        "tag": tag,
        "comment": comment,

    }
    return render(request, "post_pages/detail_post.html", context)


@login_required
def add_post(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()

        messages.success(request,
                         "Post başarıyla oluşturuldu! Düzenleyebilmen için taslak halinde profilinde seni bekliyor. "
                         "Tek yapman gereken yayına almak!")
        return redirect("my_profile")

    return render(request, "post_pages/new_post.html", {"form": form})


@login_required
def update_post(request, slug):
    #  Profile sayfası.
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if post.author != request.user:
        messages.error(request, "Bu işlem için yetkili değilsiniz!")
        return redirect("posts:detail", slug=post.slug)

    else:
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.updated_date = timezone.now()
            post.save()
            form.save_m2m()

            messages.success(request, "Post başarıyla değiştirildi!")
            return redirect("posts:detail", slug=post.slug)
        context = {
            "post": post,
            "form": form,
        }
    return render(request, "post_pages/update_post.html", context)


@login_required
def delete_post(request, slug):
    #  Silmek yerine passive yapsak daha iyi olur. Profile sayfası.
    post = get_object_or_404(Post, slug=slug)
    #  post.delete()
    if post.author == request.user:
        if post.active_post == 2:
            post.active_post = 4
            post.save()
            messages.success(request, "Post yayından kaldırıldı!")
        else:
            post.active_post = 2
            post.save()
            messages.success(request, "Post yayına alındı!")
    else:
        messages.error(request, "Bu işlem için yetkili değilsiniz!")
        return redirect("posts:detail", slug=post.slug)
    return redirect("my_profile")


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        comment_author = request.user
        comment_content = request.POST.get("comment_content")
        new_comment = Comment(comment_author=comment_author, comment_content=comment_content)
        new_comment.post = post
        new_comment.save()
        return redirect(reverse("posts:detail", kwargs={"slug": slug}))




