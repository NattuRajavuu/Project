# Luxe Atelier Python AI Commerce

A fully Python-based premium e-commerce site with Flask, Jinja templates, Tailwind CDN styling, session-backed cart and wishlist flows, and an online AI chatbot service.

## Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:8000
```

## Environment

Add keys to `.env`:

```text
OPENAI_API_KEY=
GEMINI_API_KEY=
CLAUDE_API_KEY=
SECRET_KEY=change-me-in-production
```

OpenAI is the primary provider. Gemini and Claude are supported by the Python router when their keys are configured. If no provider key is available, the chatbot uses a local fallback so the site remains usable.

## Routes

- `/`
- `/products`
- `/product/<id>`
- `/cart`
- `/checkout`
- `/login`
- `/register`
- `/profile`
- `/wishlist`
- `/chatbot`
- `POST /api/chat`
- `POST /api/chat/stream`

No React or Node.js is required.
