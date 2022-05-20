from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from job.serializers import JobSerializer, JobDetailSerializer
from job.models import Job
from account.models import User
from job.permissions import EmployerOnly, OwnerOnly
from job_assigned.models import JobAssigned, WorkingDuration
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from datetime import datetime, timedelta

# Create your views here.


class JobView(viewsets.ModelViewSet):
    def get_queryset(self):
        """
        All job created by logged in employer
        """
        return Job.objects.filter(user_associated=self.request.user)

    serializer_class = JobSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        OwnerOnly,
        EmployerOnly,
    ]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_fields = ["job_status"]
    search_fields = ["job_name", "description"]

    def create(self, request, *args, **kwargs):
        data = request.data
        # data._mutable=True # we have to do this,if data coming from form_data
        # if data coming from json ,then no need to do this
        if "member_array" in data:
            members_array = data["member_array"]
            del data["member_array"]
        else:
            members_array = None

        # data._mutable=False
        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        latest_saved_job_id = Job.objects.latest("id").id
        latest_job_id = Job.objects.get(id=latest_saved_job_id)
        if members_array is not None:
            for member_id in members_array:
                print(member_id)
                if User.objects.filter(id=member_id).exists():
                    user_id = User.objects.get(id=member_id)
                    if user_id.employer == self.request.user.email:
                        job_assigned = JobAssigned(
                            assigned_to=user_id,
                            job=latest_job_id,
                            assigned_by=self.request.user,
                        )
                        job_assigned.save()
                else:
                    pass

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(user_associated=self.request.user)


class JobDetailView(RetrieveAPIView):
    def get_queryset(self):
        return Job.objects.filter(user_associated=self.request.user)

    serializer_class = JobDetailSerializer
    permission_classes = [EmployerOnly, OwnerOnly]


class CalculateLastSevenDayWorkingHoursPerJob(APIView):
    """Caclulating LastSevenDaysWorkingHoursPerJob usng job id"""
    def get(self, request, job_id):
        print(job_id)
        current_datetime = datetime.now()
        current_datetime = current_datetime - timedelta(days=1)
        # working_obj=WorkingDuration.objects.filter(assigned_job__job__id=job_id).aggregate(sum=Sum('duration'))

        inttial_duration = timedelta(0, 0, 0)

        # # print(current_datetime)
        date_list = []
        last_seven_days_dict = []
        temporay_days_duration_dict = {}
        for i in range(7):
            days = current_datetime - timedelta(days=i)
            date = days.date()
            print(date)
            date_list.append(date)
        working_obj = WorkingDuration.objects.filter(assigned_job__job__id=job_id)

        for date in date_list:
            for assigned_job in working_obj:
                # print(assigned_job)
                assigned_date = assigned_job.timestamp.date()
                if assigned_date == date:
                    inttial_duration += assigned_job.duration
                    print("ddd", assigned_date)
                    print(inttial_duration)
                    temporay_days_duration_dict = {
                        "date": date,
                        "duration": inttial_duration,
                    }
                    temp2 = {}
                    temp2 = temporay_days_duration_dict.copy()

                else:

                    temporay_days_duration_dict = {"date": date, "duration": 0}
                    temp2 = {}
                    temp2 = temporay_days_duration_dict.copy()

            last_seven_days_dict.append(temp2)
        print(last_seven_days_dict)

        return Response(last_seven_days_dict)
