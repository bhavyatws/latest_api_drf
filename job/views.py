from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from job.serializers import JobSerializer
from job.models import Job
from job.permissions import EmployerOnlyorReadOnly,OwnerOnly

# Create your views here.
class JobView(viewsets.ModelViewSet):
    queryset=Job.objects.all()
    serializer_class=JobSerializer
    permission_classes=[permissions.IsAuthenticated,OwnerOnly,EmployerOnlyorReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user_associated=self.request.user)
    
    


