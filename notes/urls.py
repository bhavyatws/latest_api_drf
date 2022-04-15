from django.urls import path,include
from notes.views import Notesview
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('',Notesview,basename="notes")

urlpatterns=[
    path('',include(router.urls)),
]