from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import BlogPost, Comment, Like


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ["user", "content", "created_at"]


class BlogsInsightInline(admin.StackedInline):
    from blogs_insights.models import BlogsInsights
    model = BlogsInsights
    extra = 0
    readonly_fields = ["insight_title", "insight_description"]
    can_delete = False
    verbose_name = "Groq Insight"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "is_published", "published_at", "created_at", "has_insights"]
    list_filter = ["is_published"]
    search_fields = ["title", "content", "user__email"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["-created_at"]
    inlines = [CommentInline, BlogsInsightInline]
    readonly_fields = ["generate_insights_button"]
    actions = ["generate_insights_action"]

    def has_insights(self, obj):
        return hasattr(obj, "insights")
    has_insights.boolean = True
    has_insights.short_description = "Insights"

    def generate_insights_button(self, obj):
        if obj.pk:
            url = reverse("admin:blogs_blogpost_generate_insights", args=[obj.pk])
            return format_html(
                '<a class="button" href="{}" style="padding:6px 12px;background:#417690;'
                'color:#fff;border-radius:4px;text-decoration:none;">Generate Insights</a>',
                url,
            )
        return "Save the post first."
    generate_insights_button.short_description = "Groq Insights"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "<int:pk>/generate-insights/",
                self.admin_site.admin_view(self._generate_insights_view),
                name="blogs_blogpost_generate_insights",
            ),
        ]
        return custom + urls

    def _generate_insights_view(self, request, pk):
        from blogs_insights.groq_service import generate_insights
        from blogs_insights.models import BlogsInsights

        post = self.get_object(request, pk)
        if post is None:
            self.message_user(request, "Post not found.", messages.ERROR)
            return HttpResponseRedirect("../")
        try:
            data = generate_insights(post)
            BlogsInsights.objects.update_or_create(post=post, defaults=data)
            self.message_user(request, f"Insights generated for '{post.title}'.", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Failed to generate insights: {e}", messages.ERROR)
        return HttpResponseRedirect("../")

    @admin.action(description="Generate Groq insights for selected posts")
    def generate_insights_action(self, request, queryset):
        from blogs_insights.groq_service import generate_insights
        from blogs_insights.models import BlogsInsights

        success = failed = 0
        for post in queryset:
            try:
                data = generate_insights(post)
                BlogsInsights.objects.update_or_create(post=post, defaults=data)
                success += 1
            except Exception:
                failed += 1
        if success:
            self.message_user(request, f"Generated insights for {success} post(s).", messages.SUCCESS)
        if failed:
            self.message_user(request, f"Failed for {failed} post(s).", messages.ERROR)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]
    search_fields = ["user__email", "post__title", "content"]
    ordering = ["-created_at"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]
    ordering = ["-created_at"]
