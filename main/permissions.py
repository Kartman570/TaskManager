from rest_framework import permissions


class IsPermitToDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "DELETE":
            return True
        return request.user.is_staff
