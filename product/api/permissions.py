from rest_framework import permissions
from django.contrib.auth.models import User

class ReadOnlyUnlessStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not isinstance(request.user, User):
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_staff
