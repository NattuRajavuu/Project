# Luxe Atelier

A premium React + Vite ecommerce experience with a Python Flask REST backend, Tailwind CSS, Framer Motion, cart and wishlist state, dark mode, checkout simulation, and an offline-first Ollama shopping assistant.

## Run with Python

This repo now includes a Python-runnable static version that does not require Node, npm, Flask, or pip.

```bash
python app.py
```

Open:

```text
http://localhost:8000
```

## Run locally

```bash
npm install
npm run dev
```

## Backend API

The Flask backend lives in `backend/` and exposes:

- `GET /api/products`
- `GET /api/products/<id>`
- `POST /api/chat`
- `GET /api/health`

Install the backend dependencies and start the API server:

```bash
pip install -r backend/requirements.txt
python backend/app.py
```

For the local LLM assistant, install Ollama and run a model in another terminal:

```bash
ollama run llama3
```

If Ollama is not running, `/api/chat` falls back to a local rule-based product/support assistant so the UI remains usable offline.

## Frontend

Start the frontend in another terminal:

```bash
npm install
npm run dev
```

The Vite dev server proxies `/api` requests to `http://127.0.0.1:5000`.
The chatbot UI is a floating bottom-right assistant with chat history, typing state, product recommendations, and dark/light support.

## Build

```bash
npm run build
```

## Pages

- Home
- Product listing
- Product details
- Shopping cart
- Checkout
- Login / register
- User profile dashboard
- Wishlist
- Order success
