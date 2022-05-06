from django.urls import path, include
from job.views import JobView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", JobView, basename="job")

urlpatterns = [
    path("", include(router.urls)),
]
