from django.contrib import admin
from .models import Post  # Import your Post model

# Register your model here
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # This makes the admin list view show more than just "Post object (1)"
    list_display = ('content', 'author', 'created_at')
    # This adds a sidebar to filter posts by date or author
    list_filter = ('created_at', 'author')
    # This adds a search bar for the content
    search_fields = ('content',)