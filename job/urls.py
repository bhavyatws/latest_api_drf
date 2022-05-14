from django.urls import path, include
from job.views import JobView, JobDetailView, CalculateLastSevenDayWorkingHoursPerJob
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", JobView, basename="job")

urlpatterns = [
    path("<int:pk>/", JobDetailView.as_view(), name="job-detail"),
    path("last-seven-days-working-duration/<int:job_id>/", CalculateLastSevenDayWorkingHoursPerJob.as_view(), name="calculating_last_seven_days"), # noqa
    path("", include(router.urls)),
]
