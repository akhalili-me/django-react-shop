from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.validators import MinLengthValidator, RegexValidator
from products.models import CommentLike, Comment
from cart.models import Address
from products.models import Product

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$",
                message="Password must contain at least one lowercase letter, one uppercase letter, one digit, and be at least 8 characters long",
                code="invalid_password",
            ),
        ],
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "text", "rate", "likes", "author"]

    @staticmethod
    def get_author(obj):
        return obj.author.username

    @staticmethod
    def get_likes(obj):
        return obj.likes.count()

class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = ["id", "name"]

class UserCommentsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta: 
        model = Comment
        fields = ["id", "text", "rate", "likes", "product"]


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ["id", "comment", "user"]
        extra_kwargs = {"user": {"read_only": True}, "comment": {"read_only": True}}


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "state",
            "city",
            "phone",
            "postal_code",
            "street_address",
            "house_number",
        ]
