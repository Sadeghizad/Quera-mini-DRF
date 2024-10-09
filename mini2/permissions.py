from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admins to edit objects.
    Non-admins can only read (GET) objects.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  
        return request.user and request.user.is_staff  

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow:
    - Any authenticated user to view objects.
    - Only owners or admins to edit/delete objects.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are methods like GET, HEAD, OPTIONS (read-only methods)
        if request.method in SAFE_METHODS:
            return True  # Allow read-only access to anyone
        
        # Otherwise, only the owner or an admin can modify/delete
        return obj.user == request.user or request.user.is_staff
