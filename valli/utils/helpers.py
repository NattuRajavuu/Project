import json
from pathlib import Path

from flask import session


PRODUCTS_PATH = Path(__file__).resolve().parents[1] / "data" / "products.json"


def load_products():
    with PRODUCTS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)["products"]


def find_product(product_id):
    return next((product for product in load_products() if product["id"] == product_id), None)


def money(value):
    return f"${float(value):,.0f}"


def cart_items():
    raw_cart = session.get("cart", {})
    items = []
    for product_id, quantity in raw_cart.items():
        product = find_product(product_id)
        if product:
            items.append({**product, "quantity": int(quantity), "line_total": product["price"] * int(quantity)})
    return items


def cart_totals():
    items = cart_items()
    subtotal = sum(item["line_total"] for item in items)
    shipping = 18 if subtotal else 0
    return {"subtotal": subtotal, "shipping": shipping, "total": subtotal + shipping}


def cart_count():
    return sum(int(quantity) for quantity in session.get("cart", {}).values())


def product_matches(message, limit=3):
    normalized = message.lower()
    matches = []
    for product in load_products():
        haystack = f"{product['name']} {product['category']} {product['description']}".lower()
        if product["category"].lower() in normalized or any(word in haystack for word in normalized.split() if len(word) > 3):
            matches.append(product)
    return matches[:limit]
