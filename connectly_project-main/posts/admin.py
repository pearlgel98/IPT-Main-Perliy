from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # This shows who commented, on what post, and when
    list_display = ('author', 'post', 'text', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    # This shows the user and the post they liked
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at', 'user')