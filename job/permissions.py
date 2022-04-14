
from rest_framework import permissions

class EmployerOnly(permissions.BasePermission):


    def has_permission(self, request, view):
        user=request.user
        print(user.role)
        if user.role=="Employer":
            return True
            # if obj.user==user:
            #     return True
           
        return False

    def has_object_permission(self, request, view, obj):
         
           pass
            # return obj.user.role==user.role

       