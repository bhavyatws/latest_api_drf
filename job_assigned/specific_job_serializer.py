from .models import JobAssigned
from rest_framework import serializers
from job import specific_job
class UserAssignedJobSerializer(serializers.ModelSerializer):
    # job=specific_job.JobSerializer(rea)
    class Meta:
        model=JobAssigned
        fields=['id','job','timestamp']
    