from django import views
from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
from JobAssigned.models import JobAssigned
from JobAssigned.serializers import JobAssignedSerializer
from job.permissions import EmployerOnly
from JobAssigned.permissions import OwnerOnly

# Create your views here.
class JobAssignedView(viewsets.ModelViewSet):
    queryset=JobAssigned.objects.all()
    serializer_class=JobAssignedSerializer
    permission_classes=[permissions.IsAuthenticated,EmployerOnly,OwnerOnly]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)
