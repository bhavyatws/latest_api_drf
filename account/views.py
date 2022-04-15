
from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from account.serializers import UserSerializer,LevelSerializer,CertificateSerializer,ProfileSerializer, UserUploadedCertificateSerializer
from account.models import Level, User,Certification,Profile
from job.permissions import OwnerOnly

# Create your views here.

class UserView(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def perform_create(self, serializer):
        instance=serializer.save()
        instance.set_password(instance.password)
        instance.save()

class Levelview(generics.ListAPIView):
    queryset=Level.objects.all()
    serializer_class=LevelSerializer
    


class Certificationview(generics.ListAPIView):
    queryset=Certification.objects.all()
    serializer_class=CertificateSerializer
    

   

class UserUploadedCertificateview(viewsets.ModelViewSet):
    queryset=Level.objects.all()
    serializer_class=UserUploadedCertificateSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class Profileview(viewsets.ModelViewSet):
    def get_queryset(self):
        return Profile.object.filter(user=self.request.user)
    serializer_class=ProfileSerializer
    permission_classes=[permissions.IsAuthenticated,OwnerOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




    
    

