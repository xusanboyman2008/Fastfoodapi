import requests

# URL for login
url = "https://login.emaktab.uz"

# Headers (modify as needed)
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

data = {
    "login": "xusanboyabdulxayev",
    "password": "12345678x",
}

try:
    response = requests.post(url, headers=headers, data=data)
    if response.text == "":
        print("Login successful. Here is the response data:")
        # print(response.text)  # Print the raw HTML or JSON response
    else:
        print(f"Failed to login. HTTP Status Code: {response.status_code}")
        # print(f"Response: {response.text}")

except requests.RequestException as e:
    print(f"An error occurred: {e}")
