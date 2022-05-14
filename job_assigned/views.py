from account.models import User
from job.models import Job
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import generics
from job_assigned.models import JobAssigned, WorkingDuration
from job_assigned.serializers import (
    EmployerJobAssignedSerialzier,
    JobAssignedSerializer,
    JobAssignedListSerializer,
    # RemoveMemberFromAssignedJobSerializer,
)
from job.permissions import EmployerOnly
from job_assigned.permissions import OwnerOnly
from itertools import chain  # noqa
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import pytz
from datetime import timedelta, datetime
from django.db.models import Sum
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class JobAssignedView(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        queryset = (
            JobAssigned.objects.select_related("job", "assigned_to", "assigned_by")
            .filter(assigned_by=user)
            .exclude(assigned_status=False)
        )
        return queryset

    permission_classes = [
        permissions.IsAuthenticated,
        EmployerOnly,
        OwnerOnly,
    ]
    # first way
    """
    # serializer_classes = {
    #     'list': JobAssignedListSerializer,
    #     'retrieve': JobAssignedListSerializer,
    #     # ... other actions
    # }
    # default_serializer_class = JobAssignedSerializer # Your default serializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)"""
    # second way
    def get_serializer_class(self):
        if self.action == "list":
            return JobAssignedListSerializer
        if self.action == "retrieve":
            return JobAssignedListSerializer
        return JobAssignedSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data
        job_id = data["job"]
        user_id = data["assigned_to"]
        job_assigned_obj = JobAssigned.objects.filter(
            job=job_id,
            assigned_to=user_id,
            assigned_status=False,
            assigned_by=self.request.user,
        )
        if job_assigned_obj.exists():
            job_assigned_obj = job_assigned_obj[0]
            job_assigned_obj.assigned_status = True
            job_assigned_obj.save()
            return Response(
                {"response": "Job Assigned Successfully"}, status=status.HTTP_200_OK
            )
        user_obj = User.objects.filter(id=user_id, employer=self.request.user)
        if not user_obj.exists():
            return Response(
                {
                    "response": "You are not employer of this employee Or you are trying assign your job to yourself"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )  # noqa
        job_obj = Job.objects.filter(id=job_id, user_associated=self.request.user)
        if not job_obj.exists():
            return Response(
                {"response": 'another employer/"s job  assigning'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


class ListTaskAssignedView(generics.ListAPIView):
    def get_queryset(self):
        # combine_result=list(chain(JobAssigned.objects.filter(assigned_to=self.request.user),Job.objects.filter(assigned_to=self.request.user))) # noqa
        # print(combine_result)
        user_obj = self.request.user
        print(user_obj)
        return JobAssigned.objects.filter(
            assigned_to__email=user_obj, assigned_status=True
        )  # noqa

    serializer_class = JobAssignedListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["job__job_name", "job__description"]


class DetailTaskAssignedView(generics.RetrieveAPIView):
    def get_queryset(self):
        # combine_result=list(chain(JobAssigned.objects.filter(assigned_to=self.request.user),Job.objects.filter(assigned_to=self.request.user)))
        # print(combine_result)
        return JobAssigned.objects.filter(assigned_to=self.request.user).select_related(
            "job", "assigned_to", "assigned_by"
        )  # noqa

    serializer_class = JobAssignedListSerializer
    # permission_classes = [permissions.IsAuthenticated]


class StartTime(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        # pk=self.kwargs.get('id')
        data = request.data
        pk = data["job_assigned_id"]
        job_assign_obj = JobAssigned.objects.select_related(
            "job", "assigned_to", "assigned_by"
        ).filter(pk=pk, assigned_to=self.request.user, assigned_status=True)
        print(job_assign_obj)
        if job_assign_obj.exists():
            job_assign_obj = job_assign_obj[0]
            now = datetime.now(pytz.timezone("Asia/Kolkata"))
            # checking if any other assigned job he has started timer
            current_user_work_duration_obj = WorkingDuration.objects.filter(
                assigned_job__assigned_to=self.request.user, end_time=None
            )
            print(current_user_work_duration_obj)
            if current_user_work_duration_obj:
                return Response(
                    {
                        "response": "Please close the current working to start another job timer"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )  # noqa
            latest_entery_work_duration_obj = WorkingDuration(
                assigned_job=job_assign_obj, start_time=now
            )
            latest_entery_work_duration_obj.save()
            return Response(
                {
                    "started_time": now,
                    "working_duration_id": latest_entery_work_duration_obj.id,
                    "response": "job started",
                }
            )
        return Response(
            {
                "response": "This job has't been assigned to you Or you have been removed from job members"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class EndTime(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        data = request.data
        pk = data["id"]
        if JobAssigned.objects.filter(
            pk=pk, assigned_status=True, assigned_to=self.request.user
        ).exists():
            job_assign_obj = JobAssigned.objects.get(pk=pk)
            queries_workduration = WorkingDuration.objects.select_related(
                "assigned_job"
            ).filter(
                assigned_job__id=job_assign_obj.id,
                assigned_job__assigned_to=self.request.user,
                end_time=None,
            )
            if queries_workduration:
                latest_entery_work_duration_obj = queries_workduration.latest("id")
                now = datetime.now(pytz.timezone("Asia/Kolkata"))
                latest_entery_work_duration_obj.end_time = now
                latest_entery_work_duration_obj.save()
                duration = (
                    latest_entery_work_duration_obj.end_time
                    - latest_entery_work_duration_obj.start_time
                )
                print(duration)
                latest_entery_work_duration_obj.duration = duration

                latest_entery_work_duration_obj.save()
                return Response(
                    {
                        "clock out time": now,
                        "Work duration": duration,
                        "working_duration_id": latest_entery_work_duration_obj.id,
                        "response": "Clocked Out Successfully",
                    }
                )
            else:
                return Response(
                    {
                        "response": "You have not start working on this Or you have been removed from job memebers"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            return Response(
                {
                    "response": "That job has not been assigned to you so you cannot end another's job"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class CalculatingLastSevenDaysWorkingDuration(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        job_assigned = JobAssigned.objects.select_related(
            "job", "assigned_to", "assigned_by"
        ).filter(pk=pk, assigned_to=self.request.user)
        if job_assigned.exists():
            job_assigned = job_assigned[0]
            now = datetime.now()
            final_result = []
            temp_result = {}
            for i in range(7):
                current_datetime = (now - timedelta(days=i)).date()
                work_duratin_obj = (
                    WorkingDuration.objects.select_related("assigned_job")
                    .filter(
                        assigned_job__id=job_assigned.id,
                        timestamp__date=current_datetime,
                    )
                    .aggregate(duration=Sum("duration"))
                )
                temp_result["date"] = current_datetime
                temp_result["duration"] = work_duratin_obj["duration"]
                temp_result_2 = temp_result.copy()
                final_result.append(temp_result_2)
            return Response(final_result)
        return Response(
            {"response": "This job has been assigned to you"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class EmployerAssignedJobView(generics.ListAPIView):
    def get_queryset(self):
        return JobAssigned.objects.filter(assigned_by=self.request.user).exclude(
            assigned_status=False
        )

    serializer_class = EmployerJobAssignedSerialzier
    permission_classes = [
        EmployerOnly,
    ]


class RemoveMemberFromJobAssignedView(APIView):
    permission_classes = [
        EmployerOnly,
    ]

    def get(self, request, job_assigned_id):

        if job_assigned_id:

            job_assigned_obj = JobAssigned.objects.select_related("assigned_to").filter(
                job__id=job_assigned_id,
                assigned_by=self.request.user,
                assigned_status=True,
            )
            print(job_assigned_obj)
            if job_assigned_obj.exists():
                job_assigned_obj = job_assigned_obj[0]
                job_assigned_obj.assigned_status = False
                job_assigned_obj.save()
                return Response(
                    {"response": "Member removed successfully from job assigned"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "response": "Unable to Remove Member from job assigned as you might have already remove that member"  # noqa
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"response": "Please enter assigned job id and member's id to remove "},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetMembersOfParticularJobUsingJobId(APIView):
    permission_classes = [EmployerOnly, OwnerOnly]

    def get(self, request, job_id):
        job_assigned_obj = JobAssigned.objects.filter(job__id=job_id)
        # serializer=JobAssignedListSerializer(data=job_assigned_obj,many=True)
        # if serializer.is_valid():
        #     pass
        data_list = []
        for assigned_job in job_assigned_obj:

            data_list.append(assigned_job)
        return Response(
            EmployerJobAssignedSerialzier(data_list, many=True).data,
            status=status.HTTP_200_OK,
        )
