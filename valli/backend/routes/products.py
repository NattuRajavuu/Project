import json
from pathlib import Path

from flask import Blueprint, jsonify, request


products_bp = Blueprint("products", __name__)
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "products.json"


def load_products():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)["products"]


@products_bp.get("/products")
def products():
    items = load_products()
    query = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "").strip().lower()
    sort = request.args.get("sort", "featured")

    if query:
        items = [
            item
            for item in items
            if query in item["name"].lower()
            or query in item["description"].lower()
            or query in item["category"].lower()
        ]

    if category and category != "all":
        items = [item for item in items if item["category"].lower() == category]

    if sort == "low":
        items = sorted(items, key=lambda item: item["price"])
    elif sort == "high":
        items = sorted(items, key=lambda item: item["price"], reverse=True)
    elif sort == "rating":
        items = sorted(items, key=lambda item: item["rating"], reverse=True)

    return jsonify({"products": items, "total": len(items)})


@products_bp.get("/products/<product_id>")
def product_details(product_id):
    product = next((item for item in load_products() if str(item["id"]) == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)
