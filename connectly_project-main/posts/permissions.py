from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
       
        if request.user.is_staff:
            return True
        
        return obj.author == request.user

class IsVisible(permissions.BasePermission):
    """
    Ensures private posts are only visible to the author.
    """
    def has_object_permission(self, request, view, obj):
        if obj.privacy == 'public':
            return True
        return obj.author == request.user