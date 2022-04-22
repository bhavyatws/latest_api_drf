from rest_framework import serializers
from job.models import Job




class JobSerializer(serializers.ModelSerializer):
 
  class Meta:
      model=Job
      fields=['id','job_name','description','job_status','job_deadline','user_associated','timestamp',]  
      extra_kwargs={'id':{'read_only':True},'timestamp':{'read_only':True}}