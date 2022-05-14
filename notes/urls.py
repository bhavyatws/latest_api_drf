from django.urls import path, include
from notes.views import Notesview, NotesPerJobView, NotesPerAssignedJobView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", Notesview, basename="notes")

urlpatterns = [
    path("notes-per-job/", NotesPerJobView.as_view()),
    path("notes-per-assigned-job/", NotesPerAssignedJobView.as_view()),
    path("", include(router.urls)),
]
