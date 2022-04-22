from rest_framework.response import Response
from rest_framework import serializers
from account.models import FAQ, User,Level,UserUploadedCertificate,Profile,Certification
from django.forms import ValidationError
#Customizing Token Response with Role also
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from job_assigned import specific_job_serializer
from job_assigned.models import JobAssigned



class ProfileListSerializer(serializers.ModelSerializer):
    assigned_job=serializers.SerializerMethodField('get_all_assign_job')
    class Meta:
        model=Profile
        fields=('assigned_job',)
    def get_all_assign_job(self,obj):
      
        job_list=[]
        job_assigneds=JobAssigned.objects.filter(assigned_to=obj.user_associated)
        
        for job_assigned in job_assigneds:
            if job_assigned.assigned_to==obj.user_associated:

                job_list.append(job_assigned.job)
            
        return specific_job_serializer.UserAssignedJobSerializer(job_list,many=True).data
        

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='Confirm Password', write_only=True)
    profile=ProfileListSerializer(read_only=True)
   
    class Meta:

        model=User
        fields=['id','email','role','profile','password','password2']
        extra_kwargs={
            'password':{'write_only':True},
            'password2':{'write_only':True},
            'id':{'read_only':True},
            'assigned_job':{'read_only':True},
        }

    def validate(self, data):
        #validating email
        email = data.get('email', None)
        existing = User.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("Someone with that email "
                "address has already registered. Was it you?")
        # return email

        #validating password
        password = data.get('password')
        confirm_password = data.pop('password2')
        if password != confirm_password:
            raise ValidationError('Two passwords must match')
        return data

    # def get_all_assign_job(self,obj):
    #     job_list=[]
    #     job_assigneds=JobAssigned.objects.filter(assigned_to=obj)
    #     for job_assigned in job_assigneds:
    #         if job_assigned.assigned_to==self.request.user:
    #             job_list.append(job_assigned.job)
    #         return UserAssignedJobSerializer(job_list,many=True).data
       

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Level
        fields=['id','name',]


class CertificateSerializer(serializers.ModelSerializer):
    level=LevelSerializer()
    class Meta:
        model=Certification
        fields='__all__'
        

class UserUploadedCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserUploadedCertificate
        fields='__all__'
        extra_kwargs={'user':{'read_only':True}}


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Profile
        fields='__all__'
    
   
        



class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model=FAQ
        fields='__all__'
    



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    #on decoding token ,we get role also
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['Role'] = user.role
        # Add more custom fields from your custom user model, If you have a
        # custom user model.
        # ...

        return token
    #to return role in response,just overrided validate
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['Role'] = self.user.role
        
        return data

