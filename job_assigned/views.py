
from time import time
from job.models import Job
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import generics
from job_assigned.models import JobAssigned,Working_Duration
from job_assigned.serializers import JobAssignedSerializer,JobAssignedListSerializer
from job.permissions import EmployerOnlyorReadOnly
from job_assigned.permissions import OwnerOnly
from itertools import chain
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework.views import APIView
from django.utils import timezone
import pytz


# Create your views here.
class Job_assigned_view(viewsets.ModelViewSet):
    queryset=JobAssigned.objects.all()
    # serializer_class=JobAssignedSerializer
    permission_classes=[permissions.IsAuthenticated,EmployerOnlyorReadOnly,OwnerOnly]
    #first way
    '''
    # serializer_classes = {
    #     'list': JobAssignedListSerializer,
    #     'retrieve': JobAssignedListSerializer,
    #     # ... other actions
    # }
    # default_serializer_class = JobAssignedSerializer # Your default serializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)'''
    #second way
    def get_serializer_class(self):
        if self.action == 'list':
            return JobAssignedListSerializer
        if self.action == 'retrieve':
            return JobAssignedListSerializer
        return JobAssignedSerializer
    

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

class ListTaskAssignedView(generics.ListAPIView):
    def get_queryset(self):
        # combine_result=list(chain(JobAssigned.objects.filter(assigned_to=self.request.user),Job.objects.filter(assigned_to=self.request.user)))
        # print(combine_result)
        return JobAssigned.objects.filter(assigned_to=self.request.user)
    serializer_class=JobAssignedListSerializer
    # permission_classes=[permissions.IsAuthenticated]

class StartTime(APIView):
    def get(self,request,pk):
        pk=self.kwargs.get('pk')
        if JobAssigned.objects.filter(pk=pk).exists():
            job_assign_obj=JobAssigned.objects.get(pk=pk)
            now = datetime.now(pytz.timezone('Asia/Kolkata'))
            working_duration_obj=Working_Duration(assigned_job=job_assign_obj,start_time=now)
            working_duration_obj.save()
            return Response({'started_time':now,'working_duration_id':working_duration_obj.id,'response':'job started'})
        return Response({'response':'This job has\'t been assigned to you'})

class EndTime(APIView):
    def get(self,request,pk):
        pk=self.kwargs.get('pk')
        working_duration_obj=Working_Duration.objects.filter(pk=pk)
        print(working_duration_obj)
        if working_duration_obj.exists():
            working_duration_obj=Working_Duration.objects.get(pk=pk)
            now = datetime.now(pytz.timezone('Asia/Kolkata'))
            
            working_duration_obj.end_time=now
            working_duration_obj.save()
        
            duration=working_duration_obj.end_time-working_duration_obj.start_time
            print(duration)
            working_duration_obj.duration=str(duration)

            working_duration_obj.save()
            return Response({'clock out time':now,'Work duration':duration,'working_duration_id':working_duration_obj.id,'response':'Clocked Out Successfully'})
        else:
            return Response({'response':'You have not started this task to do'})