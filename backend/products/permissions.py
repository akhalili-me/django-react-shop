from rest_framework.permissions import BasePermission

class IsCommentOwner(BasePermission):
    """
    docstring
    """
    def has_permission(self, request, view):

        if view.action == 'retrieve':
            return 

        return True
