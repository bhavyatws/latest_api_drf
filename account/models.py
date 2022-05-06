
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


USER_TYPE = (
    ("Employer", "Employer"),
    ("Employee", "Employee"),
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(choices=USER_TYPE, default="Employee", max_length=30)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"


class Level(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Certification(models.Model):
    name = models.CharField(max_length=50)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserUploadedCertificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cert_image = models.ImageField(upload_to="Certification/")
    cert_name = models.ForeignKey(Certification, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "UserUploadedCertificate"

    def __str__(self):
        return f"{self.user.email}"


class Profile(models.Model):
    user_associated = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="profile"
    )
    profile_image = models.ImageField(upload_to="Profile/", blank=True, null=True)
    designation = models.CharField(max_length=100, default="", blank=True)
    phone_number = models.CharField(max_length=20, default="", blank=True)
    dob = models.DateField(blank=True, null=True)
    allergies = models.CharField(max_length=100, default="", blank=True)
    medical_issues = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return self.user_associated.email

    # resizing uploaded image after uploaded
    # def save(self,force_insert=None):
    #     super(Profile,self).save(*args, **kwargs)

    #     img = Image.open(self.profile_image.path)
    #     print(img)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_image.path)
    #         print("Resized")


class FAQ(models.Model):
    question = models.CharField(max_length=250, default="")
    answer = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.question}"
