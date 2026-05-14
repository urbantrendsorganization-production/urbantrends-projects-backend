from django.db import models
from blogs.models import BlogPost

# Create your models here.
class BlogsInsights(models.Model):
    post = models.OneToOneField(BlogPost, on_delete=models.CASCADE, related_name="insights")
    insight_title = models.CharField(max_length=200)
    insight_description = models.TextField()

    def __str__(self):
        return f"Insights for {self.post.title}"