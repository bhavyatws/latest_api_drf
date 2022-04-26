
from rest_framework import serializers
from job_assigned.models import JobAssigned
from job.serializers import JobSerializer
from account.serializers import UserSerializer
from notes.models import Notes




class JobAssignedSerializer(serializers.ModelSerializer):
    def validate(self, data):
        job=data['job']
        assigned_to=data['assigned_to']
        job_assign=JobAssigned.objects.filter(job=job ,assigned_to=assigned_to)
        if job_assign.exists():
            raise serializers.ValidationError({'error':' You cannot assign same task to same user twice'})
        return data
    class Meta:
        model=JobAssigned
        fields=['job','assigned_to']
       

class JobAssignedListSerializer(serializers.ModelSerializer):
     
    job=JobSerializer()
    # assigned_to=UserSerializer()
    assigned_by=UserSerializer()
    assigned_to=serializers.SerializerMethodField('find_all_user_associated_to_particular_task')

    # assign_job=serializers.SerializerMethodField('assign_job')
    notes_count=serializers.SerializerMethodField('count_notes')
    class Meta:
        model=JobAssigned
        fields=['id','job','assigned_to','assigned_by','timestamp','notes_count']

        extra_kwargs={'id':{'read_only':True},'assigned_by':{'read_only':True},'timestamp':{'read_only':True},
        
        
        }
    
    # def assign_job(self,obj):
    #     return Job.objects.filter(assigned_to=self.request.user)
    
    
     
    
    def count_notes(self,obj):
        return Notes.objects.filter(job_assigned=obj).count()
    
    # def get_all_notes(self,obj):
    #     list=[]
    #     notes_jobassigned_query = Notes.objects.filter(job_assigned=obj)
    #     for notes in notes_jobassigned_query:
    #         if notes.job_assigned==obj: 
    #             list.append(notes)
    #     return NotesListSerializer(list,many=True).data

    #finding all assigned_to user to particular job
    def find_all_user_associated_to_particular_task(self,obj):

        list=[]
        job_id=obj.job.id
        assign_job=JobAssigned.objects.filter(job=job_id)
       
        
        for job in assign_job:
            if job.job==obj.job:
                list.append(job.assigned_to)

        
        return UserSerializer(list,many=True).data



        
