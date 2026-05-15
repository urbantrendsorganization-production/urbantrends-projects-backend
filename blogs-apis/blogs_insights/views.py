from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import BlogsInsights
from .serializer import BlogsInsightsSerializer


class BlogInsightListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogsInsightsSerializer
    queryset = BlogsInsights.objects.select_related("post")
