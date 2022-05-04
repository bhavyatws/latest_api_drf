from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from yaml import serialize
from job.models import Job
import job_assigned
from notes.serializers import NotesSerializer,NotesListSerializer
from job.permissions import OwnerOnly
from notes.models import Notes

# Create your views here.

class Notesview(viewsets.ModelViewSet):
    queryset=Notes.objects.all()
    permission_classes=[permissions.IsAuthenticated,OwnerOnly]

    def perform_create(self, serializer):
        serializer.save(user_associated=self.request.user)

    serializer_classes = {
        'list': NotesListSerializer,
        'retrieve': NotesListSerializer,
        # ... other actions
    }
    default_serializer_class = NotesSerializer # Your default serializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

class NotesPerJob(generics.ListAPIView):
    def get_queryset(self):
        assign_job_id=self.request.query_params.get('id')
        print(assign_job_id)
        return Notes.objects.select_related('user_associated','job_assigned').filter(job_assigned=assign_job_id)
    serializer_class=NotesListSerializer
    permission_classes=[permissions.IsAuthenticated]
 
