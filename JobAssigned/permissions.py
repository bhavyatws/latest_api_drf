from rest_framework import permissions

class OwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        return obj.assigned_by==request.user
       