from django.db.models import Count
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BlogPost, Comment, Like
from .serializers import (
    BlogPostDetailSerializer,
    BlogPostListSerializer,
    BlogPostWriteSerializer,
    CommentSerializer,
    BlogsInsightsSerializer,
)


def _annotated_qs():
    return BlogPost.objects.annotate(
        likes_count=Count("likes", distinct=True),
        comments_count=Count("comments", distinct=True),
    ).select_related("user")


# ── Admin ─────────────────────────────────────────────────────────────────────

class AdminBlogListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return _annotated_qs().order_by("-created_at")

    def get_serializer_class(self):
        return BlogPostWriteSerializer if self.request.method == "POST" else BlogPostListSerializer

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)
        if post.is_published and not post.published_at:
            BlogPost.objects.filter(pk=post.pk).update(published_at=timezone.now())


class AdminBlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    lookup_field = "slug"

    def get_queryset(self):
        return _annotated_qs().prefetch_related("comments__user")

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return BlogPostWriteSerializer
        return BlogPostDetailSerializer

    def perform_update(self, serializer):
        instance = self.get_object()
        was_published = instance.is_published
        post = serializer.save()
        if post.is_published and not was_published and not post.published_at:
            BlogPost.objects.filter(pk=post.pk).update(published_at=timezone.now())


class PublicBlogsInsightsListView(generics.ListAPIView):

class AdminBlogStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total = BlogPost.objects.count()
        published = BlogPost.objects.filter(is_published=True).count()

        top_liked = (
            BlogPost.objects.annotate(cnt=Count("likes"))
            .order_by("-cnt")
            .values("title", "slug", "cnt")
            .first()
        )
        top_commented = (
            BlogPost.objects.annotate(cnt=Count("comments"))
            .order_by("-cnt")
            .values("title", "slug", "cnt")
            .first()
        )

        return Response({
            "total_posts": total,
            "published": published,
            "drafts": total - published,
            "total_likes": Like.objects.count(),
            "total_comments": Comment.objects.count(),
            "top_liked": (
                {"title": top_liked["title"], "slug": top_liked["slug"], "likes_count": top_liked["cnt"]}
                if top_liked else None
            ),
            "top_commented": (
                {"title": top_commented["title"], "slug": top_commented["slug"], "comments_count": top_commented["cnt"]}
                if top_commented else None
            ),
        })


# ── User ──────────────────────────────────────────────────────────────────────

class BlogListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogPostListSerializer

    def get_queryset(self):
        return _annotated_qs().filter(is_published=True).order_by("-published_at")


class BlogDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogPostDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            _annotated_qs()
            .filter(is_published=True)
            .prefetch_related("comments__user")
        )


class BlogCommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post__slug=self.kwargs["slug"], post__is_published=True
        ).select_related("user")

    def perform_create(self, serializer):
        post = generics.get_object_or_404(
            BlogPost, slug=self.kwargs["slug"], is_published=True
        )
        serializer.save(user=self.request.user, post=post)


class CommentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        post = generics.get_object_or_404(BlogPost, slug=slug, is_published=True)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({"liked": False, "likes_count": post.likes.count()})
        return Response(
            {"liked": True, "likes_count": post.likes.count()},
            status=status.HTTP_201_CREATED,
        )
