from django.urls import path, include
from notes.views import Notesview, NotesPerJob
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", Notesview, basename="notes")

urlpatterns = [
    path("notes-per-assigned-job/", NotesPerJob.as_view()),
    path("", include(router.urls)),
]
