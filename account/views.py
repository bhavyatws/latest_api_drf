from django.http import QueryDict
from django.shortcuts import render
from rest_framework import generics
from account.serializers import UserSerializer
from account.models import User

# Create your views here.

class UserView(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def perform_create(self, serializer):
        instance=serializer.save()
        print(instance.password)
        instance.set_password(instance.password)
        instance.save()



    
    

