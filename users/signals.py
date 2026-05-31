from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile

@receiver(post_save, sender=User)
def build_profile(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if kwargs.get('raw', False):
        return
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        pass
