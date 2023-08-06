from rest_framework import serializers
from .models import Product, ProductImage, Category, Comment, CommentLike, Feature


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


class FeatureListSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["name", "description"]


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
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["name", "products", "parent"]

    @staticmethod
    def get_products(obj):
        products = obj.products.order_by("-sold")[:3]
        product_serializer = ProductSerializer(products, many=True)
        return product_serializer.data

    @staticmethod
    def get_parent(obj):
        return obj.parent.name


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ["id", "comment", "user"]
        extra_kwargs = {"user": {"read_only": True}, "comment": {"read_only": True}}
