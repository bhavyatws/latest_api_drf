
from rest_framework import permissions

class EmployerOnly(permissions.BasePermission):


    def has_permission(self, request, view):
        user=request.user
        if user.role=="Employer":
            return True
            
           
        return False

    

class OwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        return obj.user==request.user
       