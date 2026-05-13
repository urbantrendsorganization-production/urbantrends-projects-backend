from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers

from .models import BlogPost, Comment, Like

User = get_user_model()


class HttpsImageField(serializers.ImageField):
    """Force https:// on image URLs when not in DEBUG mode."""
    def to_representation(self, value):
        url = super().to_representation(value)
        if url and not settings.DEBUG and url.startswith('http://'):
            url = 'https://' + url[7:]
        return url


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class CommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class BlogPostListSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)
    image = HttpsImageField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id", "title", "slug", "excerpt", "image", "user",
            "relevant_link", "is_published", "published_at", "created_at",
            "likes_count", "comments_count",
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)
    image = HttpsImageField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            "id", "title", "slug", "excerpt", "content", "image", "user",
            "relevant_link", "is_published", "published_at", "created_at",
            "updated_at", "likes_count", "comments_count", "is_liked", "comments",
        ]

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class BlogPostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["title", "excerpt", "content", "image", "relevant_link", "is_published"]
