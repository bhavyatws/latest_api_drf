
from rest_framework import serializers
from account.models import User,Level,UserUploadedCertificate,Profile,Certification
from django.forms import ValidationError

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='Confirm Password', write_only=True)
    class Meta:

        model=User
        fields=['email','role','password','password2']
        extra_kwargs={
            'password':{'write_only':True},
            'password2':{'write_only':True},
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

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Level
        fields=['name',]


class CertificateSerializer(serializers.ModelSerializer):
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
        extra_kwargs={'user':{'read_only':True}}

class ProfileListSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Profile
        fields='__all__'
       

