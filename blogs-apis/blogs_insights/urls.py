from django.urls import path
from .views import BlogInsightListView

urlpatterns = [
    path("insights/", BlogInsightListView.as_view(), name="blog-insights"),
]
