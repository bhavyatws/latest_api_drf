from rest_framework import serializers
from job.models import Job
from account.serializers import UserSerializer



class JobSerializer(serializers.ModelSerializer):
  user_associated=UserSerializer(read_only=True)
  members_array=serializers.ListField( required=False,child=serializers.IntegerField(min_value=0, max_value=100))
  class Meta:
      model=Job
      fields=['id','job_name','description','job_status','job_deadline','members_array','user_associated','timestamp',]  
      extra_kwargs={'id':{'read_only':True},
                      'timestamp':{'read_only':True},
                      
      
      }
  