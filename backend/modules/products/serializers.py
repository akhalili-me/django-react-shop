from rest_framework import serializers
from .models import Product, ProductImage, Category, Feature


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["uuid", "name", "image"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["slug", "name", "parent", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["slug", "name", "price", "quantity", "images"]


class ProductDetailsSerializer(ProductSerializer):
    category = serializers.StringRelatedField()
    total_comments = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + [
            "description",
            "category",
            "rate",
            "total_comments",
        ]

    @staticmethod
    def get_total_comments(obj):
        return obj.comments.count()


class FeatureSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["uuid", "name", "description"]