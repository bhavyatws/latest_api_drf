
from django.db import models
from account.models import User
from job.models import Job

# Create your models here.
class JobAssigned(models.Model):
    assigned_by=models.ForeignKey(User,on_delete=models.CASCADE)
    assigned_to=models.ForeignKey(User,on_delete=models.CASCADE,related_name="assigned_to")
    job=models.ForeignKey(Job,on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.job.job_name} to {self.assigned_to.email}'

class WorkingDuration(models.Model):
    assigned_job=models.ForeignKey(JobAssigned,on_delete=models.CASCADE,related_name="assigned_job")
    start_time=models.DateTimeField(null=True,blank=True)
    end_time=models.DateTimeField(null=True,blank=True)
    duration=models.DurationField(null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.assigned_job.job.job_name
    

