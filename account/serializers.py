from rest_framework import serializers
from account.models import (
    FAQ,
    User,
    Level,
    UserUploadedCertificate,
    Profile,
    Certification,
)

# Customizing Token Response with Role also
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ["id", "name"]


class CertificateSerializer(serializers.ModelSerializer):
    level = LevelSerializer()

    class Meta:
        model = Certification
        fields = "__all__"


class UserUploadedCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUploadedCertificate
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}


class ProfileListSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField("get_level")
    total_certificates = serializers.SerializerMethodField("get_total_no_certificate")

    class Meta:
        model = Profile
        fields = [
            "profile_image",
            "user_associated",
            "designation",
            "phone_number",
            "dob",
            "allergies",
            "medical_issues",
            "level",
            "total_certificates",
        ]  # noqa

    def get_level(self, obj):
        user_upload_list = []
        for user_upload in UserUploadedCertificate.objects.select_related(
            "user", "cert_name"
        ).filter(
            user__id=obj.user_associated.id
        ):  # noqa
            user_upload_list.append(user_upload.cert_name.level.name)
        return user_upload_list[::-1]
        # return UserUploadedCertificateSerializer(level_list,many=True).data

    def get_total_no_certificate(self, obj):
        user_upload_list = []
        for user_upload in UserUploadedCertificate.objects.select_related(
            "user", "cert_name"
        ).filter(
            user__id=obj.user_associated.id
        ):  # noqa
            user_upload_list.append(user_upload)
        return len(user_upload_list)


class ProfileListSerializerJobAssigned(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "profile_image",
        ]


class ProfileListUserSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField("get_level")
    total_certificates = serializers.SerializerMethodField("get_total_no_certificate")

    class Meta:
        model = Profile
        fields = [
            "profile_image",
            "designation",
            "phone_number",
            "dob",
            "allergies",
            "medical_issues",
            "level",
            "total_certificates",
        ]  # noqa

    def get_level(self, obj):
        user_upload_list = []
        for user_upload in UserUploadedCertificate.objects.select_related(
            "user", "cert_name"
        ).filter(
            user__id=obj.user_associated.id
        ):  # noqa
            user_upload_list.append(user_upload.cert_name.level.name)
        return user_upload_list[::-1]
        # return UserUploadedCertificateSerializer(level_list,many=True).data

    def get_total_no_certificate(self, obj):
        user_upload_list = []
        for user_upload in UserUploadedCertificate.objects.select_related(
            "user", "cert_name"
        ).filter(
            user__id=obj.user_associated.id
        ):  # noqa
            user_upload_list.append(user_upload)
        return len(user_upload_list)


class UserListSerializerJobAssigned(serializers.ModelSerializer):
    profile = ProfileListSerializerJobAssigned(read_only=True)

    class Meta:
        model = User
        fields = ["id", "profile"]


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label="Confirm Password", write_only=True)
    profile = ProfileListUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "role", "profile", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
            "id": {"read_only": True},
            "assigned_job": {"read_only": True},
        }  # noqa

    def validate(self, data):
        # validating email
        email = data.get("email", None)
        existing = User.objects.filter(email=email).only("email").first()
        if existing:
            raise serializers.ValidationError(
                "Someone with that email  address has already registered. Was it you?"
            )
        # return email

        # validating password
        password = data.get("password")
        confirm_password = data.pop("password2")
        if password != confirm_password:
            raise serializers.ValidationError("Two passwords must match")
        return data

    # def get_all_assign_job(self,obj):
    #     job_list=[]
    #     job_assigneds=JobAssigned.objects.filter(assigned_to=obj)
    #     for job_assigned in job_assigneds:
    #         if job_assigned.assigned_to==self.request.user:
    #             job_list.append(job_assigned.job)
    #         return UserAssignedJobSerializer(job_list,many=True).data


class NotesUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # on decoding token ,we get role also
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["Role"] = user.role
        # Add more custom fields from your custom user model, If you have a
        # custom user model.
        # ...

        return token

    # to return role in response,just overrided validate

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        # Add extra responses here
        data["Role"] = self.user.role
        return data


class InviteByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs['email']
        print(email)
        user = User.objects.filter(email=email)
        if user:
            raise serializers.ValidationError("User with this email already exist")
        return attrs
