from django.contrib import admin
from .models import Post, Category, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "category_name"]
    list_display_links = ["id", "category_name"]

    class Meta:
        model = Category


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "category_name", "sub_category_image","sub_category_name"]
    list_display_links = ["id", "category_name", "sub_category_name"]

    class Meta:
        model = SubCategory


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "title", "author", "created_date", "updated_date", "active_post"]

    class Meta:
        model = Post
