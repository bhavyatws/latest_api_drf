from rest_framework import permissions


class EmployerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        # if view.action == 'list':
        #     return True

        # if view.action == 'retrieve':
        #     return True

        if user.role == "Employer":
            return True

        return False


class OwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.user_associated == request.user
