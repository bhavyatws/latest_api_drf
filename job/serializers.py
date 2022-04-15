from rest_framework import serializers
from job.models import Job
from account.serializers import UserSerializer



class JobSerializer(serializers.ModelSerializer):
  user=UserSerializer()
  class Meta:
      model=Job
      fields=['id','job_name','description','job_status','job_deadline','user','timestamp',]  
      extra_kwargs={'id':{'read_only':True},'user':{'read_only':True},'timestamp':{'read_only':True}}