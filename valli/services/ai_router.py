import logging

from services import claude_service, gemini_service, openai_service
from utils.helpers import load_products, product_matches


SYSTEM_PROMPT = """You are Luxe Chat, a premium e-commerce AI assistant.
Answer concisely with an elegant, helpful tone. Recommend only products from the local catalog.
Support product discovery, comparisons, checkout, shipping, returns, and account questions.
If asked for exact availability outside the local catalog, say you can only use the current store catalog."""


def catalog_context():
    return "\n".join(
        f"- {item['name']} | {item['category']} | ${item['price']} | rating {item['rating']} | {item['description']}"
        for item in load_products()
    )


def build_messages(message, history):
    recent = history[-10:] if history else []
    return [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nCatalog:\n{catalog_context()}"},
        *recent,
        {"role": "user", "content": message},
    ]


def fallback_reply(message):
    products = product_matches(message)
    lower = message.lower()
    if products:
        names = ", ".join(item["name"] for item in products)
        return f"I would start with {names}. These match your request and fit the quiet luxury profile of the collection.", products
    if any(word in lower for word in ["shipping", "delivery", "arrive"]):
        return "Orders ship in premium recyclable packaging and typically arrive within 3-5 business days.", []
    if any(word in lower for word in ["return", "refund", "cancel"]):
        return "Returns are available within 30 days for items in original condition. I can also help you choose an exchange.", []
    if any(word in lower for word in ["checkout", "payment", "card"]):
        return "Checkout is a secure demo flow in this Python app. Add products to cart, then continue to checkout.", []
    return "I can help with recommendations, product comparisons, checkout, shipping, returns, and wishlist ideas.", []


def generate_reply(message, history=None, provider="openai"):
    messages = build_messages(message, history or [])
    products = product_matches(message)
    providers = {
        "openai": openai_service.complete,
        "gemini": gemini_service.complete,
        "claude": claude_service.complete,
    }
    order = [provider, "openai", "gemini", "claude"]
    seen = set()

    for name in order:
        if name in seen or name not in providers:
            continue
        seen.add(name)
        try:
            return providers[name](messages), products, name
        except Exception as error:
            logging.info("%s provider unavailable: %s", name, error)

    reply, fallback_products = fallback_reply(message)
    return reply, products or fallback_products, "fallback"


def stream_reply(message, history=None, provider="openai"):
    messages = build_messages(message, history or [])
    products = product_matches(message)

    if provider in ("openai", ""):
        try:
            yield {"type": "meta", "provider": "openai", "products": products}
            for token in openai_service.stream(messages):
                yield {"type": "token", "content": token}
            return
        except Exception as error:
            logging.info("OpenAI streaming unavailable: %s", error)

    reply, products, source = generate_reply(message, history, provider)
    yield {"type": "meta", "provider": source, "products": products}
    for token in reply.split(" "):
        yield {"type": "token", "content": token + " "}
