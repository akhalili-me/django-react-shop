from rest_framework import serializers
from .models import Product, ProductImage, Category, Feature


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

    class Meta:
        model = Product
        fields = ["id", "name", "price", "quantity", "images"]


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


class FeatureListSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["name", "description"]


# class TopSellingProductsByChildCategorySerializer(serializers.ModelSerializer):
#     products = serializers.SerializerMethodField()
#     parent = serializers.SerializerMethodField()

#     class Meta:
#         model = Category
#         fields = ["name", "products", "parent"]

#     @staticmethod
#     def get_products(obj):
#         products = obj.products.order_by("-sold")[:3]
#         product_serializer = ProductSerializer(products, many=True)
#         return product_serializer.data

#     @staticmethod
#     def get_parent(obj):
#         return obj.parent.name
