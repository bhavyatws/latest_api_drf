from notes.models import Notes
from account.serializers import UserSerializer
from job_assigned.serializers import JobAssignedListSerializer
from rest_framework import serializers

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields=['job','notes','user_associated']
        extra_kwargs={'user':{'read_only':True}}

class NotesListSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    job=JobAssignedListSerializer()
    class Meta:
        model=Notes
        fields='__all__'
       