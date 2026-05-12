from django.contrib import admin
from .models import BlogPost, Comment, Like


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ["user", "content", "created_at"]


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "is_published", "published_at", "created_at"]
    list_filter = ["is_published"]
    search_fields = ["title", "content", "user__email"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["-created_at"]
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]
    search_fields = ["user__email", "post__title", "content"]
    ordering = ["-created_at"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]
    ordering = ["-created_at"]
