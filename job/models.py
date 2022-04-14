from tabnanny import verbose
from django.db import models
from psycopg2 import Timestamp
from account.models import User

job_status_choice=(
    ("New","New"),
    ("Progress","Progress"),
    ("Complete","Complete"),
)
# Create your models here.

class Job(models.Model):
    job_name=models.CharField(max_length=100)
    description=models.TextField()
    job_status=models.CharField(choices=job_status_choice,max_length=30)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    job_deadline=models.DateField()
    timestamp=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="Job"
        ordering=('timestamp',)

    def __str__(self):
        return f'{self.job_name} By {self.user.email}'