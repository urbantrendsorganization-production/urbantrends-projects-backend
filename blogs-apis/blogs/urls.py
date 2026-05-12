from django.urls import path
from . import views

urlpatterns = [
    # Admin
    path("admin/blogs/stats/", views.AdminBlogStatsView.as_view(), name="admin-blog-stats"),
    path("admin/blogs/", views.AdminBlogListCreateView.as_view(), name="admin-blog-list-create"),
    path("admin/blogs/<slug:slug>/", views.AdminBlogDetailView.as_view(), name="admin-blog-detail"),

    # Users
    path("blogs/", views.BlogListView.as_view(), name="blog-list"),
    path("blogs/<slug:slug>/", views.BlogDetailView.as_view(), name="blog-detail"),
    path("blogs/<slug:slug>/comments/", views.BlogCommentListCreateView.as_view(), name="blog-comments"),
    path("blogs/<slug:slug>/like/", views.LikeToggleView.as_view(), name="blog-like"),
    path("blogs/comments/<int:pk>/", views.CommentDeleteView.as_view(), name="comment-delete"),
]
