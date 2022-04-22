
from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from yaml import serialize
from account.serializers import UserSerializer,LevelSerializer,CertificateSerializer,ProfileSerializer, UserUploadedCertificateSerializer,ProfileListSerializer,FAQSerializer,MyTokenObtainPairSerializer
from account.models import Level, User,Certification,Profile,UserUploadedCertificate,FAQ
from job.permissions import OwnerOnly
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView#customizing Token

# Create your views here.

class UserView(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def perform_create(self, serializer):
        instance=serializer.save()
        print(instance)
        instance.set_password(instance.password)
        instance.save()

class Levelview(generics.ListAPIView):
    queryset=Level.objects.all()
    serializer_class=LevelSerializer
    


class Certificationview(generics.ListAPIView):
    queryset=Certification.objects.all()
    serializer_class=CertificateSerializer
    

   

class UserUploadedCertificateview(viewsets.ModelViewSet):
    queryset=UserUploadedCertificate.objects.all()
    serializer_class=UserUploadedCertificateSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProfileListView(generics.ListAPIView):
    def get_queryset(self):
        return Profile.objects.filter(user_associated=self.request.user)
    serializer_class=ProfileListSerializer
    permission_classes=[permissions.IsAuthenticated,OwnerOnly]

class Profileview(generics.UpdateAPIView):
    def get_queryset(self):
        pk=self.kwargs.get('pk')
        return Profile.objects.filter(pk=pk)
    serializer_class=ProfileSerializer
    permission_classes=[permissions.IsAuthenticated,OwnerOnly]



class FAQView(generics.ListAPIView):
    queryset=FAQ.objects.all()
    serializer_class=FAQSerializer

#Customizing Token Response
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



    
    

