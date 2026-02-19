from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'author_name', 'created_at']
        read_only_fields = ['author']

    def validate_content(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Content must be at least 5 characters.")
        return value

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'author_name', 'created_at']

        

class RegisterSerializer(serializers.ModelSerializer):                    # We add a password field that is 'write_only' so it never leaks in GET requests
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # ERROR HANDLING/SECURITY: 
        # Use create_user (not create) to handle password hashing automatically
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

        