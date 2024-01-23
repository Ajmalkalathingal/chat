from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from .models import User,UserProfile
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or update UserProfile when a User is created or saved.
    """    
    try:
        user_profile = instance.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None

    if created or user_profile is None:
        # If the user is created or UserProfile does not exist, create a UserProfile instance
        UserProfile.objects.get_or_create(user=instance)
    else:
        # If the user is saved (updated) and UserProfile exists, update it
        user_profile.save()



