import requests

post_id = 1  # Change this to the ID of the post you want to edit
url = f"http://127.0.0.1:8000/posts/{post_id}/"
token_key = "YOUR_TOKEN_HERE"

headers = {"Authorization": f"Token {token_key}"}
data = {"content": "This post has been updated successfully! 🚀"}

response = requests.put(url, json=data, headers=headers)

print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("Success! Data updated:", response.json())
else:
    print("Failed:", response.text)