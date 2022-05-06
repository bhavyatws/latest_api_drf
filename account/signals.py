from account.models import User, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

# while creating user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user_associated=instance)
        print("profile created")


# while updating user
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
        print("profile saved")
    except ObjectDoesNotExist:
        Profile.objects.create(user_associated=instance)
