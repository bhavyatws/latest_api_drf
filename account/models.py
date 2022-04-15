from pyexpat import model
from tabnanny import verbose
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


USER_TYPE=(
    ("Employer","Employer"),
    ("Employee","Employee"),
)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role=models.CharField(choices=USER_TYPE,default="Employee",max_length=30)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Level(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Certification(models.Model):
    name=models.CharField(max_length=50)
    level=models.ForeignKey(Level,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserUploadedCertificate(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cert_image=models.ImageField(upload_to="Certification/")
    cert_name=models.ForeignKey(Certification,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="UserUploadedCertificate"

    def __str__(self):
        return f'{self.user.email}'

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_img=models.ImageField(upload_to="Profile/")
    designation=models.CharField(max_length=100,default="")
    phone_number=models.CharField(max_length=20,default="")
    dob=models.DateField(blank=True)
    allergies=models.CharField(max_length=100,default="")
    medical_issues=models.CharField(max_length=100,default="")

    def __str__(self):
        return self.user.email
