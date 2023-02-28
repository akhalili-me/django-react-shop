from rest_framework import serializers
from .models import *

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','name', 'image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','parent']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id','name','description','category','price','quantity','images']
    
    def get_category(self, obj):
        return obj.category.name
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = self.get_category(instance)
        return representation
    

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id','text','rate','like','author']

    def get_author(self,obj):
        return obj.author.username
    
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['author'] = self.get_author(instance)
        return representation
        

