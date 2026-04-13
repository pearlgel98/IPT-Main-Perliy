import requests
TASK_API_URL = "http://127.0.0.1:8001/tasks/"

def get_user_tasks(user_id):
    try:
        response = requests.get(f"{TASK_API_URL}?user={user_id}")
        return response.json()
    except:
        return []