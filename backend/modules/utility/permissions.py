from rest_framework.permissions import BasePermission

class IsSuperuserOrObjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser: 
            return True

        # Check if the user on the model is equal to the request.user
        return obj.user == request.user