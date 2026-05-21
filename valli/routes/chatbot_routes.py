import time
from collections import defaultdict, deque

from flask import Blueprint, Response, jsonify, render_template, request, session

from services.ai_router import generate_reply


chatbot_bp = Blueprint("chatbot", __name__)
RATE_LIMIT = defaultdict(deque)


def allowed(ip):
    now = time.time()
    calls = RATE_LIMIT[ip]
    while calls and now - calls[0] > 60:
        calls.popleft()
    if len(calls) >= 20:
        return False
    calls.append(now)
    return True


@chatbot_bp.get("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")


@chatbot_bp.post("/api/chat")
def api_chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    provider = str(payload.get("provider", "openai")).strip().lower()
    if not message:
        return jsonify({"error": "Message is required", "reply": "Please enter a message."}), 400
    if not allowed(request.remote_addr or "local"):
        return jsonify({"error": "Rate limit exceeded", "reply": "Please wait a moment before sending another message."}), 429

    history = session.setdefault("chat_history", [])
    reply, products, source = generate_reply(message, history, provider)
    history.extend([{"role": "user", "content": message}, {"role": "assistant", "content": reply}])
    session["chat_history"] = history[-16:]
    return jsonify({"reply": reply, "products": products, "provider": source})


@chatbot_bp.post("/api/chat/stream")
def api_chat_stream():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    provider = str(payload.get("provider", "openai")).strip().lower()
    if not message:
        return jsonify({"error": "Message is required"}), 400
    if not allowed(request.remote_addr or "local"):
        return jsonify({"error": "Rate limit exceeded"}), 429

    history = session.setdefault("chat_history", [])
    reply, products, source = generate_reply(message, history, provider)
    history.extend([{"role": "user", "content": message}, {"role": "assistant", "content": reply}])
    session["chat_history"] = history[-16:]

    def event_stream():
        import json

        yield f"data: {json.dumps({'type': 'meta', 'provider': source, 'products': products})}\n\n"
        for token in reply.split(" "):
            yield f"data: {json.dumps({'type': 'token', 'content': token + ' '})}\n\n"
        yield f"data: {json.dumps({'type': 'done', 'provider': source, 'products': products})}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")


@chatbot_bp.post("/api/chat/clear")
def clear_chat():
    session["chat_history"] = []
    return jsonify({"status": "cleared"})
