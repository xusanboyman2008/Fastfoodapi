import requests
import json


def fetch_all_data():
    # API endpoint for products
    products_url = "http://127.0.0.1:8000/api/products/"
    # API endpoint for recipes
    recipes_url = "http://127.0.0.1:8000/api/recipes/"
    # API endpoint for ingredients
    ingredients_url = "http://127.0.0.1:8000/api/ingredient/"

    # Bearer token for authentication
    token = "e506c111a38b9420682e88f0f7b727009b47e754"  # Replace with your actual token

    # Headers with the Bearer token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        # Fetching products data
        products_response = requests.get(products_url, headers=headers)
        if products_response.status_code != 200:
            print(
                f"Failed to fetch products. Status code: {products_response.status_code}, Message: {products_response.text}")
            return

        products = products_response.json()  # Assuming the API returns JSON data

        # Loop through each product
        for product in products:
            print("------------------------------")
            print("Product Details:")
            product_copy = product.copy()

            # Fetching the related recipe data
            if "recipe" in product and product["recipe"]:
                recipe_response = requests.get(f"{recipes_url}{product['recipe']}/", headers=headers)
                if recipe_response.status_code == 200:
                    recipe_data = recipe_response.json()
                    product_copy["recipe_details"] = recipe_data

                    # Fetching ingredients for the recipe
                    if "ingredients" in recipe_data and isinstance(recipe_data["ingredients"], list):
                        detailed_ingredients = []
                        for ingredient_id in recipe_data["ingredients"]:
                            ingredient_response = requests.get(f"{ingredients_url}{ingredient_id}/", headers=headers)
                            if ingredient_response.status_code == 200:
                                detailed_ingredients.append(ingredient_response.json())
                            else:
                                detailed_ingredients.append(
                                    {"id": ingredient_id, "error": "Failed to fetch ingredient details"})
                        product_copy["recipe_details"]["ingredients_details"] = detailed_ingredients
                else:
                    product_copy["recipe_details"] = f"Failed to fetch (Status code: {recipe_response.status_code})"

            # Pretty print the product details
            print(json.dumps(product_copy, indent=4))
            print("------------------------------")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    fetch_all_data()
