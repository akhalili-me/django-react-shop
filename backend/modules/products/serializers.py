from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "name", "image"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    num_comments = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "price",
            "quantity",
            "images",
            "rate",
            "num_comments",
        ]

    @staticmethod
    def get_num_comments(obj):
        return obj.comments.count()
    
    def validate_category(self, value):
        category = get_object_or_404(Category, pk=value)
        if category.parent is None:
            raise serializers.ValidationError("Parent category cannot be set as product category")
        return category

class FeatureListSerilizer(serializers.ModelSerializer):
    class Meta: 
        model = Feature
        fields = ['name','description']


class ProductCommentListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    liked_by_current_user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "text", "rate", "likes", "author", "liked_by_current_user"]

    @staticmethod
    def get_author(obj):
        return obj.author.username

    @staticmethod
    def get_likes(obj):
        return obj.likes.count()

    def get_liked_by_current_user(self, obj):
        user = self.context["request"].user
        if user.is_authenticated and obj.likes.filter(user_id=user.id).exists():
            return True
        return False


class ProductCommentCreateSerializer(serializers.ModelSerializer):
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
    
class TopSellingProductsByChildCategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ["name","products"]

    @staticmethod
    def get_products(obj):
        products = obj.products.order_by("-sold")[:3]
        product_serializer = ProductSerializer(products, many=True)
        return product_serializer.data