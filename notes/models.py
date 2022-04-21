from operator import mod
from django.db import models
from account.models import User
from job_assigned.models import JobAssigned

# Create your models here.

class Notes(models.Model):
    user_associated=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    job_assigned=models.ForeignKey(JobAssigned,on_delete=models.CASCADE,related_name='notes')#giving related so we can use job serializer also
    notes=models.TextField()
    timestamp=models.DateTimeField(auto_now=True)

    def __str__(self):
       return f'{self.notes} By {self.user_associated.email}'

