
from account.models import User,Profile
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import os
from django.core.exceptions import ObjectDoesNotExist
#while creating user
@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user_associated=instance)

#while updating user
@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user_associated=instance)


