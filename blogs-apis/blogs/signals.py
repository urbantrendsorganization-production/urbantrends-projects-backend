from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from accounts.models import Subscriber
from accounts.email_service import send_new_blog_email
from .models import BlogPost

_was_published = {}


@receiver(pre_save, sender=BlogPost)
def track_publish_state(sender, instance, **kwargs):
    if instance.pk:
        _was_published[instance.pk] = BlogPost.objects.filter(
            pk=instance.pk, is_published=True
        ).exists()


@receiver(post_save, sender=BlogPost)
def on_blog_published(sender, instance, created, **kwargs):
    previously_published = _was_published.pop(instance.pk, False)
    just_published = instance.is_published and (created or not previously_published)

    if just_published:
        if not instance.published_at:
            BlogPost.objects.filter(pk=instance.pk).update(published_at=timezone.now())
            instance.refresh_from_db(fields=["published_at"])

        subscribers = list(Subscriber.objects.values_list("email", flat=True))
        send_new_blog_email(instance, subscribers)
