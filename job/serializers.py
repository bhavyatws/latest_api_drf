from rest_framework import serializers
from job.models import Job
from job_assigned.models import JobAssigned, WorkingDuration
from account.serializers import UserSerializer
from django.db.models import Sum


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

        job_assigns_query = (
            JobAssigned.objects.select_related("assigned_to", "job", "assigned_by")
            .filter(job__id=obj.id)
            .exclude(assigned_status=False)
        )
        for job_assign in job_assigns_query:
            if obj.id == job_assign.job.id:
                members.append(job_assign.assigned_to)

        return UserSerializer(members, many=True).data


class JobDetailSerializer(serializers.ModelSerializer):

    """This serializer for   job_detail"""

    total_hours_in_seconds = serializers.SerializerMethodField(
        "get_total_hours_per_job"
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "job_name",
            "description",
            "job_status",
            "total_hours_in_seconds",
        ]

    def get_total_hours_per_job(self, obj):
        working_duration_obj = WorkingDuration.objects.filter(
            assigned_job__job__id=obj.id
        ).aggregate(sum=Sum("duration"))
        print(working_duration_obj["sum"])
        return working_duration_obj["sum"]


class JobListAssignedSerializer(serializers.ModelSerializer):
    """This serializer is being using in assigned job serizlie"""

    class Meta:
        model = Job
        fields = ["id", "job_name", "description"]
