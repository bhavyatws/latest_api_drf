
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from account.serializers import UserSerializer,LevelSerializer,CertificateSerializer,ProfileSerializer, UserUploadedCertificateSerializer,ProfileListSerializer,FAQSerializer,MyTokenObtainPairSerializer
from account.models import Level, User,Certification,Profile,UserUploadedCertificate,FAQ
from job.permissions import OwnerOnly
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView#customizing Token
from rest_framework import filters
from rest_framework.views import APIView
from job_assigned.models import WorkingDuration
from datetime import datetime, timedelta
from rest_framework.response import Response
from django.db.models import Sum

# Create your views here.

class UserView(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['email']

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
    def get_queryset(self):
        return UserUploadedCertificate.objects.select_related('user','cert_name').filter(user=self.request.user)
    serializer_class=UserUploadedCertificateSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProfileListView(generics.ListAPIView):
    def get_queryset(self):
        return Profile.objects.select_related('user_associated').filter(user_associated=self.request.user)
    serializer_class=ProfileListSerializer
    permission_classes=[permissions.IsAuthenticated,OwnerOnly]

class Profileview(generics.UpdateAPIView):
    def get_queryset(self):
        pk=self.kwargs.get('pk')
        return Profile.objects.select_related('user_associated').filter(pk=pk)
    serializer_class=ProfileSerializer
    permission_classes=[permissions.IsAuthenticated,OwnerOnly]


class WorkingDurationPerEmployee(APIView):
    def get(self,request,pk):
        now=datetime.now()
        user_obj=User.objects.get(pk=pk)
        final_result=[]
        temp_result_1={}
        for i in range(7):
            current_datetime=now-timedelta(days=i)
            working_obj=WorkingDuration.objects.select_related('assigned_job').filter(assigned_job__assigned_to__id=user_obj.id,timestamp__date=current_datetime).aggregate(duration=Sum('duration'))
            current_datetime=current_datetime.date()
            temp_result_1['date']=current_datetime
            temp_result_1['duration']=working_obj['duration']
            
            temp_result_2=temp_result_1.copy()#copying dict to temp dict and appending that dict to final_result list
            final_result.append(temp_result_2)
        return Response(final_result)


class FAQView(generics.ListAPIView):
    queryset=FAQ.objects.all()
    serializer_class=FAQSerializer

#Customizing Token Response
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer





    
    

