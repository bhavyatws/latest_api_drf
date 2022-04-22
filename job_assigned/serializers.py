
from pyexpat import model
from rest_framework import serializers
from job_assigned.models import JobAssigned
from job.serializers import JobSerializer
from account.serializers import UserSerializer
from notes.models import Notes
from notes.serializers import NotesListSerializer
from account.models import Profile


class JobAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model=JobAssigned
        fields=['job','assigned_to']
       

class JobAssignedListSerializer(serializers.ModelSerializer):
    job=JobSerializer()
    # assigned_to=UserSerializer()
    assigned_by=UserSerializer()
    assigned_to=serializers.SerializerMethodField('find_all_user_associated_to_particular_task')
    
    notes=serializers.SerializerMethodField('get_all_notes')
    notes_count=serializers.SerializerMethodField('count_notes')
    class Meta:
        model=JobAssigned
        fields=['id','job','assigned_to','assigned_by','timestamp','notes','notes_count']
        extra_kwargs={'id':{'read_only':True},'assigned_by':{'read_only':True},'timestamp':{'read_only':True}}
    
    
     
    
    def count_notes(self,obj):
        return Notes.objects.filter(job_assigned=obj).count()
    
    def get_all_notes(self,obj):
        list=[]
        notes_jobassigned_query = Notes.objects.filter(job_assigned=obj)
        for notes in notes_jobassigned_query:
            if notes.job_assigned==obj: 
                list.append(notes)
        return NotesListSerializer(list,many=True).data

    #finding all assigned_to user to particular job
    def find_all_user_associated_to_particular_task(self,obj):

        list=[]
        job_id=obj.job.id
        assign_job=JobAssigned.objects.filter(job=job_id)


        for job in assign_job:
            if job.job==obj.job:
                list.append(job.assigned_to)
        
        return UserSerializer(list,many=True).data



        
