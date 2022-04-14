from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from job.serializers import JobSerializer
from job.models import Job
from job.permissions import EmployerOnly

# Create your views here.
class JobView(viewsets.ModelViewSet):
    queryset=Job.objects.all()
    serializer_class=JobSerializer
    permission_classes=[EmployerOnly,permissions.IsAuthenticated,]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    


