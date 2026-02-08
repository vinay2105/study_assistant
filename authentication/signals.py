from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile
from allauth.account.signals import user_signed_up
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) 
@receiver(user_signed_up)
def populate_google_profile(request, user, **kwargs):
    """Google login → ensure profile exists."""
    Profile.objects.get_or_create(user=user)