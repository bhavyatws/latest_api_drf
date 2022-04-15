from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from notes.serializers import NotesSerializer,NotesListSerializer
from job.permissions import OwnerOnly
from notes.models import Notes

# Create your views here.

class Notesview(viewsets.ModelViewSet):
    queryset=Notes.objects.all()
    permission_classes=[permissions.IsAuthenticated,OwnerOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    serializer_classes = {
        'list': NotesListSerializer,
        'retrieve': NotesListSerializer,
        # ... other actions
    }
    default_serializer_class = NotesSerializer # Your default serializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)