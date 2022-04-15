from pyexpat import model
from rest_framework import serializers
from JobAssigned.models import JobAssigned
from job.serializers import JobSerializer
from account.serializers import UserSerializer

class JobAssignedSerializer(serializers.ModelSerializer):
    job=JobSerializer()
    assigned_to=UserSerializer()
    assigned_by=UserSerializer()
    class Meta:
        model=JobAssigned
        fields=['id','job','assigned_to','assigned_by','timestamp']
        extra_kwargs={'id':{'read_only':True},'assigned_by':{'read_only':True},'timestamp':{'read_only':True}}