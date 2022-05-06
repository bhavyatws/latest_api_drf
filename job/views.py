from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from job.serializers import JobSerializer
from job.models import Job
from account.models import User
from job.permissions import EmployerOnlyorReadOnly, OwnerOnly
from job_assigned.models import JobAssigned
from rest_framework import filters

# Create your views here.


class JobView(viewsets.ModelViewSet):
    def get_queryset(self):
        return Job.objects.filter(user_associated=self.request.user)

    serializer_class = JobSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        OwnerOnly,
        EmployerOnlyorReadOnly,
    ]
    filter_backends = [filters.SearchFilter]
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
