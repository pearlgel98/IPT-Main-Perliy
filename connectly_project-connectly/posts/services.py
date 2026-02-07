from .models import Post

class APISettings:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APISettings, cls).__new__(cls)
            cls._instance.max_content_length = 500
        return cls._instance

class PostFactory:
    @staticmethod
    def create_post(user, content):
        settings = APISettings()  
        if len(content) > settings.max_content_length:
            raise ValueError("Content exceeds allowed limit.")
        return Post.objects.create(author=user, content=content)