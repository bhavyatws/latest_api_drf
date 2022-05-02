


from django.http import JsonResponse
from job.models import Job,User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import generics
from job_assigned.models import JobAssigned,WorkingDuration
from job_assigned.serializers import JobAssignedSerializer,JobAssignedListSerializer
from job.permissions import EmployerOnlyorReadOnly
from job_assigned.permissions import OwnerOnly
from itertools import chain
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework.views import APIView
import pytz
from datetime import timedelta,datetime
from django.db.models import Sum
from rest_framework import filters




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
    
    def create(self, request, *args, **kwargs):
        data=self.request.data
        job_id=data['job']
        user_id=data['assigned_to']
        user_obj=User.objects.filter(id=user_id)
        if user_obj.exists:
            user_obj=User.objects.get(id=user_id)
            if user_obj==self.request.user:
                return Response({'response':'you are trying  assign your job to yourself '},status=status.HTTP_400_BAD_REQUEST)

        job_obj=Job.objects.filter(id=job_id)
        if not job_obj.exists:
            job_obj=Job.objects.get(id=job_id)
            if job_obj.user_associated!=self.request.user:
                return Response({'response':'another employer/"s job  assigning'},status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

class ListTaskAssignedView(generics.ListAPIView):
    def get_queryset(self):
        # combine_result=list(chain(JobAssigned.objects.filter(assigned_to=self.request.user),Job.objects.filter(assigned_to=self.request.user)))
        # print(combine_result)
        return JobAssigned.objects.filter(assigned_to=self.request.user).prefetch_related('job')
    serializer_class=JobAssignedListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['job__job_name', 'job__description']

class DetailTaskAssignedView(generics.RetrieveAPIView):
    def get_queryset(self):
        # combine_result=list(chain(JobAssigned.objects.filter(assigned_to=self.request.user),Job.objects.filter(assigned_to=self.request.user)))
        # print(combine_result)
        return JobAssigned.objects.filter(assigned_to=self.request.user)
    serializer_class=JobAssignedListSerializer
    
    # permission_classes=[permissions.IsAuthenticated]

class StartTime(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def post(self,request):
        # pk=self.kwargs.get('id')
        data=request.data
        pk=data['id']
       
        if JobAssigned.objects.filter(pk=pk,assigned_to=self.request.user).exists():
            job_assign_obj=JobAssigned.objects.get(pk=pk)
            now = datetime.now(pytz.timezone('Asia/Kolkata'))
            #checking if anyother assigned job he has started timer
            current_user_work_duration_obj=WorkingDuration.objects.filter(assigned_job__assigned_to=self.request.user,end_time=None)
            print(current_user_work_duration_obj)
           
            if current_user_work_duration_obj:
                return Response({'response':'Please close the current working to start another job timer'},status=status.HTTP_400_BAD_REQUEST)
           
            latest_entery_work_duration_obj=WorkingDuration(assigned_job=job_assign_obj,start_time=now)
            latest_entery_work_duration_obj.save()
            return Response({'started_time':now,'working_duration_id':latest_entery_work_duration_obj.id,'response':'job started'})
        return Response({'response':'This job has\'t been assigned to you'},status=status.HTTP_400_BAD_REQUEST)

class EndTime(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    def post(self,request):
        data=request.data
        pk=data['id']
       
        if JobAssigned.objects.filter(pk=pk).exists():
            job_assign_obj=JobAssigned.objects.get(pk=pk)
            queries_workduration=WorkingDuration.objects.filter(assigned_job=job_assign_obj,assigned_job__assigned_to=self.request.user,end_time=None)
            if queries_workduration:
                latest_entery_work_duration_obj=queries_workduration.latest('id')
            
                    
                now = datetime.now(pytz.timezone('Asia/Kolkata'))
                
                latest_entery_work_duration_obj.end_time=now
                latest_entery_work_duration_obj.save()
            
                duration=latest_entery_work_duration_obj.end_time-latest_entery_work_duration_obj.start_time
                print(duration)
                latest_entery_work_duration_obj.duration=duration

                latest_entery_work_duration_obj.save()
                return Response({'clock out time':now,'Work duration':duration,'working_duration_id':latest_entery_work_duration_obj.id,'response':'Clocked Out Successfully'})
            else:
                return Response({'response':'You have not start working on this'})

        else:
            return Response({'response':'That job has not been assigned to you '},status=status.HTTP_400_BAD_REQUEST)

class CalculatingLastSevenDaysWorkingDuration(APIView):
    def get(self,request,pk):

        job_assigned=JobAssigned.objects.get(pk=pk)
        now = datetime.now()
        final_result=[]
        temp_result={}
        for  i in range(7):
       
            current_datetime=(now-timedelta(days=i)).date()

            work_duratin_obj=WorkingDuration.objects.filter(assigned_job=job_assigned,timestamp__date=current_datetime).aggregate(duration=Sum('duration'))
          
           
            temp_result['date']=current_datetime
            temp_result['duration']=work_duratin_obj['duration']
            temp_result_2=temp_result.copy()
            final_result.append(temp_result_2)
             
        return Response(final_result)
       

        
       
            
        
