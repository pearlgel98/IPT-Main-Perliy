import requests

url = "http://127.0.0.1:8000/posts/"
token_key = "YOUR_TOKEN_HERE"  # Replace with your actual token

headers = {"Authorization": f"Token {token_key}"}
data = {"content": "Creating our first post to test the API!"}

response = requests.post(url, json=data, headers=headers)

print(f"Status Code: {response.status_code}")
print("Response:", response.json())