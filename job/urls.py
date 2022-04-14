from django.urls import path,include
from job import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('',views.JobView,basename="job")

urlpatterns = [
    path('',include(router.urls)),
]
