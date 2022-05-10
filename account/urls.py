from django.urls import path, include
from account.views import (
    UserView,
    Levelview,
    UserUploadedCertificateview,
    Certificationview,
    Profileview,
    FAQView,
    ProfileListView,
    WorkingDurationPerEmployee,
    InviteByEmailView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    "user-upload-certificate", UserUploadedCertificateview, basename="certification"
)
# router.register('profile',Profileview,basename="profile")
urlpatterns = [
    path("user/", UserView.as_view()),
    path("invite-by-email/", InviteByEmailView.as_view()),
    path("level/", Levelview.as_view()),
    path("profile/", ProfileListView.as_view()),
    path("profile/<int:pk>/", Profileview.as_view()),
    path("faq/", FAQView.as_view()),
    path("certification/", Certificationview.as_view()),
    path(
        "working-duration-per-employee/<int:pk>/", WorkingDurationPerEmployee.as_view()
    ),
    path("", include(router.urls)),
]
