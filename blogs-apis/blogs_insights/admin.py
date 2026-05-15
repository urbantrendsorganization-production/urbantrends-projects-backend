from django.contrib import admin
from .models import BlogsInsights


@admin.register(BlogsInsights)
class BlogsInsightsAdmin(admin.ModelAdmin):
    list_display = ["post", "insight_title"]
    search_fields = ["post__title", "insight_title"]
    readonly_fields = ["post", "insight_title", "insight_description"]
