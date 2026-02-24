from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment

# 1. User Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):                
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# 2. Comment Serializer 
class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'text', 'created_at']

# 3. Post Serializer
class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'author_name', 'created_at', 'comments']
        read_only_fields = ['author']

    def validate_content(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Content must be at least 5 characters.")
        return value