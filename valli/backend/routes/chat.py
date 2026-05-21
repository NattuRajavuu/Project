from flask import Blueprint, jsonify, request

try:
    from services.ollama_service import ask_shopping_assistant
except ModuleNotFoundError:
    from backend.services.ollama_service import ask_shopping_assistant


chat_bp = Blueprint("chat", __name__)


@chat_bp.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Message is required", "reply": "Please send a message."}), 400

    reply, metadata = ask_shopping_assistant(message)
    return jsonify(
        {
            "reply": reply,
            "response": reply,
            "source": metadata.get("source", "fallback"),
            "products": metadata.get("products", []),
        }
    )
