from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import CartItem

class isCartOwner(BasePermission):
    """
    Custom permission to only allow cart owners of an object to access it.
    """
    def has_permission(self, request, view):
        id = view.kwargs.get('pk')
        cart_item = get_object_or_404(CartItem,id=id)
        return cart_item.session.user == request.user
        
