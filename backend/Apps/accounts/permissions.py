from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_permission(self, request, view):
        # Allow GET and POST requests
        if request.method in ["GET", "POST"]:
            return True

        # Check if user has appropriate permissions for edit and delete
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user == view.get_object()
        )
