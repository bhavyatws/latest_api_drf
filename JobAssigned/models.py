from operator import mod
from django.db import models
from account.models import User
from job.models import Job

# Create your models here.
class JobAssigned(models.Model):
    assigned_by=models.ForeignKey(User,on_delete=models.CASCADE)
    assigned_to=models.ForeignKey(User,on_delete=models.CASCADE,related_name="assigned_to")
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.job.job_name} to {self.assigned_to.email}'