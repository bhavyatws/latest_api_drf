from django.urls import path,include
from job_assigned.views import EndTime, Job_assigned_view,ListTaskAssignedView, StartTime,Calculating_last_seven_days_working_duration
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('',Job_assigned_view,basename="job")

urlpatterns = [
    
    path('assigned-job-list/',ListTaskAssignedView.as_view()),
    path('start-time/<int:pk>/',StartTime.as_view()),
    path('end-time/<int:pk>/',EndTime.as_view()),
    path('last_seven_days_working_duration_per_obj/<int:pk>/',Calculating_last_seven_days_working_duration.as_view()),
    path('',include(router.urls)),
]
