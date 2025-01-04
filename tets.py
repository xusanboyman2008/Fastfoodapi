import requests

# URL for the endpoint that handles product creation (assuming the correct endpoint)
url = 'http://127.0.0.1:8000/products/'

# Data for creating a product with nested ingredients and recipes
data = {
    "name": "Product A",
    "price": 19.99,
    "ingredients": [
        {
            "name": "Recipe 1",
            "changes": "Initial recipe",
            "ingredient": [
                {
                    "measure": 100,
                    "measure_unit": {"id": 1},  # ID for the measurement unit (e.g., grams)
                    "ingredient": {"id": 1}      # ID for the ingredient (e.g., flour)
                }
            ]
        }
    ]
}

# Send POST request to the API
response = requests.post(url, json=data)

# Check if the response is successful (status code 201)
if response.status_code == 201:
    print("Product created:", response.json())
else:
    print(f"Error {response.status_code}: {response.text}")
