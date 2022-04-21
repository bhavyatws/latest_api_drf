from django.urls import path,include
from job_assigned.views import Job_assigned_view,ListTaskAssignedView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('',Job_assigned_view,basename="job")

urlpatterns = [
    # path('',include(router.urls)),
    path('assigned-job-list/',ListTaskAssignedView.as_view())
]
