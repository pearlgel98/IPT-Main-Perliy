from .models import Post

class APISettings:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APISettings, cls).__new__(cls)
            cls._instance.max_content_length = 500
        return cls._instance
    
TASK_API_URL = "http://localhost:8001/tasks/"

class PostFactory:
    @staticmethod
    def create_post(user, content):
        settings = APISettings()  
        if len(content) > settings.max_content_length:
            raise ValueError("Content exceeds allowed limit.")
        return Post.objects.create(author=user, content=content)
    
    class TaskService:
        
    @staticmethod
    def get_user_tasks(user_id):
        try:
            response = requests.get(f"{TASK_API_URL}?user_id={user_id}")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_task(task_id):
        try:
            response = requests.get(f"{TASK_API_URL}{task_id}/")
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            return {"error": str(e)}
        