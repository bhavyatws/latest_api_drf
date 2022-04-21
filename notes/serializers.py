from notes.models import Notes
from account.serializers import UserSerializer
from job_assigned.serializers import JobAssignedListSerializer
from rest_framework import serializers

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields=['job_assigned','notes','user_associated']
        extra_kwargs={'user_associated':{'read_only':True}}

class NotesListSerializer(serializers.ModelSerializer):
    user_associated=UserSerializer()
    job_assigned=JobAssignedListSerializer()
    class Meta:
        model=Notes
        fields='__all__'
       