
from rest_framework import permissions

#this part is for authorization

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Normal users can only read (GET requests).
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return request.user and request.user.is_authenticated
        
        # Write permissions are only allowed for admin users
        return request.user and request.user.is_authenticated and request.user.is_staff
