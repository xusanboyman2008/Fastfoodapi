import requests

# URL for login
url = "http://127.0.0.1:8000/auth/login/"

# Headers (modify as needed)
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

data = {
    "username": "test",
    "password": "123",
}

try:
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("Login successful. Here is the response data:")
        print(response.text)  # Print the raw HTML or JSON response
    else:
        print(f"Failed to login. HTTP Status Code: {response.status_code}")
        print(f"Response: {response.text}")

except requests.RequestException as e:
    print(f"An error occurred: {e}")
