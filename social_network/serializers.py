from rest_framework import serializers
from .models import Post


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostLikeUnLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'likes', )