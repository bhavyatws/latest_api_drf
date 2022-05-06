from django.db import models
from account.models import User
from job.models import Job

# Create your models here.


class JobAssigned(models.Model):
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_to"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}-{self.job.job_name} to {self.assigned_to.email}"

    # @property
    # def find_all_members(self):
    #     list=[]
    #     job_id=self.job.id
    #     assign_job=JobAssigned.objects.filter(job=job_id).select_related('assigned_to','assigned_by','job')

    #     for job in assign_job:
    #         if job.job==self.job:
    #             list.append(job.assigned_to)
    #     return list


class WorkingDuration(models.Model):
    assigned_job = models.ForeignKey(
        JobAssigned, on_delete=models.CASCADE, related_name="assigned_job"
    )
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.id}-{self.assigned_job.job.job_name}"
