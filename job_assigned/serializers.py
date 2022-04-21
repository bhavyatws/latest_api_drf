
from rest_framework import serializers
from job_assigned.models import JobAssigned
from job.serializers import JobSerializer
from account.serializers import UserSerializer
from notes.models import Notes


class JobAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model=JobAssigned
        fields=['job','assigned_to']
       

class JobAssignedListSerializer(serializers.ModelSerializer):
    job=JobSerializer()
    # assigned_to=UserSerializer()
    assigned_by=UserSerializer()
    assigned_to=serializers.SerializerMethodField('find_all')
    notes=serializers.SerializerMethodField('count_notes')
    class Meta:
        model=JobAssigned
        fields=['id','job','assigned_to','assigned_by','timestamp','notes']
        extra_kwargs={'id':{'read_only':True},'assigned_by':{'read_only':True},'timestamp':{'read_only':True}}
    
    #finding all assigned_to user to particular job
    def find_all(self,obj):
        list=[]
        for assign in JobAssigned.objects.all():
            if assign.job==obj.job:
               list.append(assign.assigned_to.email)
        return list
    
    def count_notes(self,obj):
        return Notes.objects.filter(job_assigned=obj).count()
    

        
