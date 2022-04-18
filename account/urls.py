from django.urls import path,include
from account.views import UserView,Levelview,UserUploadedCertificateview,Certificationview,Profileview
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('user-upload-certificate',UserUploadedCertificateview,basename="certification")
# router.register('profile',Profileview,basename="profile")
urlpatterns = [
    path('user/',UserView.as_view()),
    path('level/',Levelview.as_view()),
    path('profile/<int:pk>/',Profileview.as_view()),
    path('certification/',Certificationview.as_view()),
    path('',include(router.urls)),
]
