from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import CartItem
from django.http import Http404

class isCartOwner(BasePermission):
    """
    Custom permission to only allow cart owners of an object to access it.
    """
    def has_permission(self, request, view):
        product_id = view.kwargs.get('pk')

        try:
            cart_item = CartItem.objects.get(product__id=product_id)
        except CartItem.DoesNotExist:
            raise Http404()
        
        return cart_item.session.user == request.user
        
