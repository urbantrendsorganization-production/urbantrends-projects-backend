from django.db.models.signals import post_save
from django.dispatch import receiver

from blogs.models import BlogPost
from .models import BlogsInsights
from .groq_service import generate_insights

_was_published = {}


@receiver(post_save, sender=BlogPost, dispatch_uid="blogs_insights.track_publish")
def track_publish_state(sender, instance, **kwargs):
    if instance.pk:
        _was_published[instance.pk] = BlogPost.objects.filter(
            pk=instance.pk, is_published=True
        ).exists()


@receiver(post_save, sender=BlogPost, dispatch_uid="blogs_insights.generate_on_publish")
def generate_insights_on_publish(sender, instance, created, **kwargs):
    previously = _was_published.pop(instance.pk, False)
    just_published = instance.is_published and (created or not previously)
    if not just_published:
        return

    try:
        data = generate_insights(instance)
        BlogsInsights.objects.update_or_create(
            post=instance,
            defaults=data,
        )
    except Exception:
        pass
