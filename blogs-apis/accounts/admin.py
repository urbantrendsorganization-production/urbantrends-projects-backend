from django.contrib import admin
from .models import Subscriber, UserProfile


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "subscribed_at"]
    search_fields = ["email"]
    ordering = ["-subscribed_at"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "website"]
    search_fields = ["user__email"]
