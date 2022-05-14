from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from notes.serializers import NotesSerializer, NotesListSerializer
from job.permissions import EmployerOnly, OwnerOnly
from notes.models import Notes
# from django.db.models import Q

# from rest_framework import status
# from rest_framework.response import Response

# Create your views here.


class Notesview(viewsets.ModelViewSet):
    def get_queryset(self):
        notes = Notes.objects.select_related("user_associated").filter(
            user_associated=self.request.user
        )
        if notes.exists():
            return notes
        else:
            print("yes")
            return None

    permission_classes = [permissions.IsAuthenticated, OwnerOnly]

    def perform_create(self, serializer):
        serializer.save(user_associated=self.request.user)

    serializer_classes = {
        "list": NotesListSerializer,
        "retrieve": NotesListSerializer,
        # ... other actions
    }
    default_serializer_class = NotesSerializer  # Your default serializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class NotesPerAssignedJobView(generics.ListAPIView):
    def get_queryset(self):
        assign_job_id = self.request.query_params.get("id")
        print(assign_job_id)
        notes = Notes.objects.select_related("user_associated", "job_assigned").filter(
            job_assigned=assign_job_id, user_associated=self.request.user
        )
        if notes.exists:
            return notes
        return 404

    serializer_class = NotesListSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotesPerJobView(generics.ListAPIView):
    def get_queryset(self):
        job_id = self.request.query_params.get("id")
        print(job_id)
        # notes = Notes.objects.select_related("job_assigned").filter(
        #     Q(job_assigned__job__id=job_id)|Q(job_assigned=job_id)
        # )
        notes = Notes.objects.select_related("job_assigned").filter(
            job_assigned__job__id=job_id
        )
        if notes.exists:
            return notes
        return 404

    serializer_class = NotesListSerializer
    permission_classes = [
        EmployerOnly, OwnerOnly
    ]
