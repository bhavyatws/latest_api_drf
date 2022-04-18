from stripe import Recipient
from account.models import User,Profile
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import os

#while creating user
@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

#while updating user
@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()

@receiver(pre_save,sender=Profile)
def delete_old_profileimg(sender,instance,**kwargs):
    #on creation,signal won't be created
    if instance._state.adding and not instance.pk:
        return False
    try:
        old_image=sender.objects.get(pk=instance.pk).profile_image
    except sender.DoesNotExist:
        return False
    #comparing old file with new file
    image = instance.profile_image
    if not old_image == image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)