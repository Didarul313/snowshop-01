import json

def load_products():
    """Load product data from the JSON file."""
    with open('products.json', 'r') as file:
        return json.load(file)

def add_to_cart(cart, product_id, products):
    """Add a product to the cart based on product ID."""
    for product in products:
        if product["id"] == product_id:
            cart.append(product)
            return True
    return False

def calculate_total(cart):
    """Calculate the total price of items in the cart."""
    return sum(item['price'] for item in cart)