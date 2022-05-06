from rest_framework import serializers
from job.models import Job
from job_assigned.models import JobAssigned
from account.serializers import UserSerializer


class JobSerializer(serializers.ModelSerializer):
    user_associated = UserSerializer(read_only=True)
    members_array = serializers.ListField(
        required=False, child=serializers.IntegerField(min_value=0, max_value=100)
    )
    members = serializers.SerializerMethodField("get_assigned_members")

    class Meta:
        model = Job
        fields = [
            "id",
            "job_name",
            "description",
            "job_status",
            "job_deadline",
            "members_array",
            "members",
            "user_associated",
            "timestamp",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "timestamp": {"read_only": True},
        }

    def get_assigned_members(self, obj):
        members = []

        job_assigns_query = JobAssigned.objects.select_related(
            "assigned_to", "job", "assigned_by"
        ).filter(job__id=obj.id)
        for job_assign in job_assigns_query:
            if obj.id == job_assign.job.id:
                members.append(job_assign.assigned_to)

        return UserSerializer(members, many=True).data


class JobListAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id", "job_name", "description"]
