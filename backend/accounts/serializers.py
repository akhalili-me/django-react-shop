from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.validators import MinLengthValidator,RegexValidator

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[
        MinLengthValidator(8),
        RegexValidator(
            regex='^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$',
            message='Password must contain at least one lowercase letter, one uppercase letter, one digit, and be at least 8 characters long',
            code='invalid_password'
        )
    ])
        
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password']

