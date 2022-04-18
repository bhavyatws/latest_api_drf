
from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
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

class Profileview(generics.RetrieveUpdateAPIView):
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):

        if self.request.method == 'GET':
            return ProfileListSerializer
        return ProfileSerializer
    
    permission_classes=[permissions.IsAuthenticated,OwnerOnly]



class FAQView(generics.ListAPIView):
    queryset=FAQ.objects.all()
    serializer_class=FAQSerializer

#Customizing Token Response
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



    
    

