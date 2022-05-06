from rest_framework import serializers
from job_assigned.models import JobAssigned, WorkingDuration
from account.serializers import UserListSerializerJobAssigned
from notes.models import Notes
from django.db.models import Sum


class JobAssignedSerializer(serializers.ModelSerializer):
    def validate(self, data):
        job = data["job"]
        assigned_to = data["assigned_to"]
        job_assign = JobAssigned.objects.filter(job=job, assigned_to=assigned_to)
        if job_assign.exists():
            raise serializers.ValidationError(
                {"error": " You cannot assign same task to same user twice"}
            )
        return data

    class Meta:
        model = JobAssigned
        fields = ["job", "assigned_to"]


class JobAssignedListSerializer(serializers.ModelSerializer):

    # job=JobListAssignedSerializer(read_only=True)
    # assigned_to=UserListSerializerJobAssigned()
    # assigned_by=UserSerializer()
    members = serializers.SerializerMethodField(
        "find_all_user_associated_to_particular_task"
    )
    assign_job_status = serializers.SerializerMethodField("get_assign_job_status")
    notes_count = serializers.SerializerMethodField("count_notes")
    total_hours_worked_in_second = serializers.SerializerMethodField(
        "get_total_hours_worked"
    )
    # members=UserListSerializerJobAssigned(source='find_all_members',many=True)

    class Meta:
        model = JobAssigned
        fields = [
            "id",
            "job",
            "members",
            "timestamp",
            "notes_count",
            "assign_job_status",
            "total_hours_worked_in_second",
        ]
        # fields=['members']

        extra_kwargs = {
            "id": {"read_only": True},
            "assigned_by": {"read_only": True},
            "timestamp": {"read_only": True},
        }

    def count_notes(self, obj):
        return (
            Notes.objects.filter(job_assigned=obj)
            .select_related("job_assigned", "user_associated")
            .only("job_assigned")
            .count()
        )

    def get_assign_job_status(self, obj):
        query = WorkingDuration.objects.select_related("assigned_job").filter(
            assigned_job=obj, end_time=None
        )
        if query.exists():
            return "Progress"
        return "Stop"

    def get_total_hours_worked(self, obj):
        work_duration_obj = (
            WorkingDuration.objects.select_related("assigned_job")
            .filter(assigned_job__id=obj.job.id)
            .only("duration")
            .aggregate(duration=Sum("duration"))
        )
        return work_duration_obj["duration"]

    # def get_all_notes(self,obj):
    #     list=[]
    #     notes_jobassigned_query = Notes.objects.filter(job_assigned=obj)
    #     for notes in notes_jobassigned_query:
    #         if notes.job_assigned==obj:
    #             list.append(notes)
    #     return NotesListSerializer(list,many=True).data

    # finding all assigned_to user to particular job

    def find_all_user_associated_to_particular_task(self, obj):

        list = []
        job_id = obj.job.id
        assign_job = JobAssigned.objects.select_related("job", "assigned_to").filter(
            job=job_id
        )

        for job in assign_job:
            if job.job == obj.job:
                list.append(job.assigned_to)

        return UserListSerializerJobAssigned(list, many=True).data

    # def get_working_duration_of_seven_days(self,obj):
    #     now = timezone.now()
    # today=Working_Duration.objects.filter(timestamp=now.date())
    # yesterday=Working_Duration.objects.filter(timestamp__gte=(now - timedelta(hours=24)).date())
    # last_7_day= WorkingDuration.objects.filter(timestamp__gte=(now - timedelta(days=7)).date()),
    # working_duration=[today,yesterday,last_7_day]

    # last_seven_days_duration_obj_list=[]
    # for query in last_7_day:
    #     for quer in query:
    #         # if query.assigned_job==obj:
    #         if quer.assigned_job==obj:
    #             last_seven_days_duration_obj_list.append(quer)

    # #calcuting timestamp from today to last_seven days
    # worked_history_last_seven_days={}

    # duration=timedelta(0,0)
    # print(duration)
    # for i in range(7):
    #     calcutated_timestamp=now-timedelta(days=i)
    #     print("calculated date",calcutated_timestamp.date())
    #     # print(calcutated_timestamp,type(calcutated_timestamp))

    #     for query in last_seven_days_duration_obj_list:
    #         print("object's date ",query.timestamp.date())
    #         if query.timestamp.date()==calcutated_timestamp.date():
    #             print("***")
    #             duration= duration + query.duration
    #             print("$$$$",duration)
    #             worked_history_last_seven_days[str(calcutated_timestamp)]=duration

    # print(worked_history_last_seven_days)
    # return worked_history_last_seven_days
