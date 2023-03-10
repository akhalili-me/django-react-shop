from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()
class UserViewSet(ModelViewSet):
    """
    Viewset for creating, editing, deleting and fetching a user.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self,request,*args, **kwargs):
        """
        Hash the password before saving it.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=kwargs.get('partial', False))
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if request.data.get('password'):
                user.set_password(request.data.get('password'))
                user.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
