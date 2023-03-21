from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import status,generics
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from products.serializers import CommentSerializer
from products.models import Comment

User = get_user_model()
class UserViewSet(ModelViewSet):
    """
    Viewset for creating, editing, deleting and fetching a user.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get('password'))
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()

    def create(self, request, *args, **kwargs):
        """
        Add user and hash the password.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def update(self, request, *args, **kwargs):
        """
        Update user and hash the password.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
class UserCommentsListView(generics.ListAPIView):
    """
    Return the comments associated with the authenticated user.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)
    

class RUDCommentsView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieve, update and destroy comments. 
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(id=self.kwargs.get('pk'),author=self.request.user)
