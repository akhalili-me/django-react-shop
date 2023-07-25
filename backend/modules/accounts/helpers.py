from .models import User

def create_user_from_serializer(serializer):
    email = serializer.validated_data["email"]
    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]
    User.objects.create_user(email, password, username)