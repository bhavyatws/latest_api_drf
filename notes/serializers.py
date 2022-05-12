from account.models import Profile
from notes.models import Notes
from account.serializers import NotesUserSerializer
from rest_framework import serializers


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ["job_assigned", "notes", "user_associated"]
        extra_kwargs = {"user_associated": {"read_only": True}}

    def validate(self, attrs):
        currently_authenticated_user = self.context['request'].user
        job_assinged_obj = attrs['job_assigned']
        if not job_assinged_obj.assigned_to == currently_authenticated_user:
            raise serializers.ValidationError("You are not allowed to comment on other's job")
        return attrs


class NotesListSerializer(serializers.ModelSerializer):
    # user_associated=UserSerializer()
    user_associated = NotesUserSerializer(read_only=True)
    profile_image = serializers.SerializerMethodField("get_profile_image")

    class Meta:
        model = Notes
        fields = [
            "id",
            "user_associated",
            "profile_image",
            "job_assigned",
            "notes",
            "timestamp",
        ]

    def get_profile_image(self, obj):
        profile_obj = Profile.objects.select_related("user_associated").get(
            user_associated=obj.user_associated
        )
        print(profile_obj.profile_image)
        if profile_obj.profile_image:
            return str(profile_obj.profile_image)
