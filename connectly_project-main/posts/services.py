from .models import Post, Comment, Like

# SINGLETON PATTERN: Configuration
class APISettings:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APISettings, cls).__new__(cls)
            cls._instance.max_content_length = 500
            cls._instance.max_comment_length = 200 # <-- ADDITION
        return cls._instance

# FACTORY PATTERN: Centralized Creation
class PostFactory:
    @staticmethod
    def create_post(user, content):
        settings = APISettings()
        if len(content) > settings.max_content_length:
            raise ValueError("Content exceeds allowed limit.")
        return Post.objects.create(author=user, content=content)

    # --- ADDITION: Comment Factory ---
    @staticmethod
    def create_comment(user, post, text):
        settings = APISettings()
        if not text:
            raise ValueError("Comment text cannot be empty.")
        if len(text) > settings.max_comment_length:
            raise ValueError(f"Comment exceeds {settings.max_comment_length} characters.")
        
        return Comment.objects.create(author=user, post=post, text=text)

    # --- ADDITION: Like Toggle Logic ---
    @staticmethod
    def toggle_like(user, post):
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
            return "Unliked"
        return "Liked"