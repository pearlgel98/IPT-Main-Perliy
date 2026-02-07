import requests

post_id = 1  # Change this to the ID you want to delete
url = f"http://127.0.0.1:8000/posts/{post_id}/"
token_key = "YOUR_TOKEN_HERE"

headers = {"Authorization": f"Token {token_key}"}

response = requests.delete(url, headers=headers)

print(f"Status Code: {response.status_code}")

if response.status_code == 204:
    print("Successfully deleted. No content left to show.")
else:
    print("Delete failed. Check if ID exists and you own the post.")