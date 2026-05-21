import json
from pathlib import Path

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
PRODUCTS_PATH = Path(__file__).resolve().parents[1] / "data" / "products.json"


def _products():
    with PRODUCTS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)["products"]


def _matches(message):
    normalized = message.lower()
    return [
        product
        for product in _products()
        if product["category"].lower() in normalized
        or product["name"].lower() in normalized
        or any(word in product["description"].lower() for word in normalized.split() if len(word) > 3)
    ][:3]


def _fallback_reply(message):
    products = _matches(message)
    normalized = message.lower()

    if products:
        names = ", ".join(product["name"] for product in products)
        return f"I would start with {names}. They match the premium, minimal style of the collection.", products
    if any(word in normalized for word in ["shipping", "delivery", "arrive"]):
        return "Orders ship in premium recyclable packaging and usually arrive within 3-5 business days.", []
    if any(word in normalized for word in ["return", "refund", "cancel"]):
        return "Returns are accepted within 30 days as long as the item is in original condition.", []
    if any(word in normalized for word in ["checkout", "payment", "card"]):
        return "Checkout is a local demo flow with secure-payment styling and no cloud payment dependency.", []

    return "I can help with product recommendations, comparisons, shipping, returns, wishlist ideas, and checkout questions.", []


def ask_shopping_assistant(message):
    products = _matches(message)
    catalog = "\n".join(
        f"- {item['name']} ({item['category']}): ${item['price']}, rating {item['rating']}. {item['description']}"
        for item in _products()
    )
    prompt = (
        "You are a concise luxury e-commerce shopping assistant. "
        "Recommend only from this local catalog and answer support questions clearly.\n\n"
        f"Catalog:\n{catalog}\n\n"
        f"Customer: {message}\n"
        "Assistant:"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        reply = str(data.get("response", "")).strip()
        if reply:
            return reply, {"source": "ollama", "products": products}
    except requests.RequestException:
        pass

    reply, fallback_products = _fallback_reply(message)
    return reply, {"source": "local-fallback", "products": products or fallback_products}
