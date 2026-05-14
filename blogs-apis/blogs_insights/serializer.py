from rest_framework import serializers
from .models import BlogsInsights

# Serializer for BlogsInsights model
class BlogsInsightsSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = BlogsInsights
        fields = ['id', 'post', 'post_title', 'insight_title', 'insight_description']
        read_only_fields = ['id', 'post_title']