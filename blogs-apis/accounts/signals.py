from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

from .models import Subscriber, UserProfile
from .email_service import send_welcome_email, send_subscription_welcome_email

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(user_signed_up)
def on_user_signed_up(request, user, **kwargs):
    send_welcome_email(user)


@receiver(post_save, sender=Subscriber)
def on_subscriber_created(sender, instance, created, **kwargs):
    if created:
        send_subscription_welcome_email(instance.email)
