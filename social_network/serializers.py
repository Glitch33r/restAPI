from .models import Post
from testAPI import settings
from pyhunter import PyHunter
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

hunter = PyHunter(settings.HUNTER_KEY)


class PostListSerializer(serializers.ModelSerializer):
    # detail_view = serializers.HyperlinkedIdentityField(view_name='social_network:post-detail', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'name', 'author_name', )


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'name', 'text', 'likes', 'author_name',)


class PostLikeUnLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'likes',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',)

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate_email(self, value):
        """
        Check if email exists
        """
        resp = hunter.email_verifier(value)
        if User.objects.filter(email=value).exists() or resp.get('result') in ['undeliverable', 'risky']:
            raise serializers.ValidationError("Not unique email or email does not exist in email-services")
        return value
