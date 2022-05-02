from account.models import Profile
from notes.models import Notes
from account.serializers import NotesUserSerializer
from rest_framework import serializers

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields=['job_assigned','notes','user_associated']
        extra_kwargs={'user_associated':{'read_only':True}}

class NotesListSerializer(serializers.ModelSerializer):
    # user_associated=UserSerializer()
    user_associated=NotesUserSerializer(read_only=True)
    profile_image=serializers.SerializerMethodField('get_profile_image')

    class Meta:
        model=Notes
        fields=['id','user_associated','profile_image','job_assigned','notes','timestamp']

    
       
    def get_profile_image(self,obj):
        profile_obj=Profile.objects.get(user_associated=obj.user_associated)
        if profile_obj.profile_image:
            return profile_obj.profile_image
       