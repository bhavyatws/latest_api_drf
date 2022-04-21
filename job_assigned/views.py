from django import views
from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import generics
from job_assigned.models import JobAssigned
from job_assigned.serializers import JobAssignedSerializer,JobAssignedListSerializer
from job.permissions import EmployerOnlyorReadOnly
from job_assigned.permissions import OwnerOnly
from rest_framework import serializers

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
        print(self.request.user)
        serializer.save(assigned_by=self.request.user)

class ListTaskAssignedView(generics.ListAPIView):
    def get_queryset(self):
        print(self.request.user)
        return JobAssigned.objects.filter(assigned_to=self.request.user)
    serializer_class=JobAssignedListSerializer
    # permission_classes=[permissions.IsAuthenticated]
