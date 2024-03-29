from rest_framework.permissions import BasePermission,SAFE_METHODS
from functools import reduce

class IsSuperUserOrObjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_superuser:
            return True

        user_field = getattr(view, "user_field", "user")

        if user_field == "user":
            return request.user == getattr(obj, user_field)

        object_owner = reduce(getattr, user_field.split("."), obj)
        return request.user == object_owner


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return request.user and request.user.is_superuser
