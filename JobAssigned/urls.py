from django.urls import path,include
from JobAssigned.views import JobAssignedView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('',JobAssignedView,basename="job")

urlpatterns = [
    path('',include(router.urls)),
]
