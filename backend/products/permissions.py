from rest_framework.permissions import BasePermission


class SuperuserEditOnly(BasePermission):
    """
    Allows access only to superusers for create, update, and delete,
    but allows all users to list and retrieve.
    """

    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.is_superuser
        return True
