import json
import os
import re
import sqlite3
import subprocess
from pathlib import Path
from typing import Optional

MODEL_CMD = os.environ.get('LOCAL_AI_MODEL_CMD')
MODEL_PATH = os.environ.get('GPT4ALL_MODEL_PATH')

RESPONSE_FALLBACK = {
    'shipping': 'Shipping is free for orders over $100 and usually arrives within 3-5 business days. If you need it faster, ask me about expedited delivery options.',
    'refund': 'Refunds are handled within 5-7 business days after approval. You can request a return from the order page or by sending me your order ID.',
    'payment': 'We accept credit cards, debit cards, Apple Pay, Google Pay, and secure local checkout options for offline-ready orders.',
    'tracking': 'Please share your order ID and I will look up the latest tracking status from the offline order database.',
    'warranty': 'All products include a one-year limited warranty covering manufacturing defects and quality issues.',
}

SEARCH_FIELDS = ['name', 'category', 'description', 'tag']


def sanitize_text(text: str) -> str:
    return re.sub(r'<.*?>', '', text).strip()


def run_local_model(prompt: str) -> Optional[str]:
    if not MODEL_PATH and not MODEL_CMD:
        return None

    command = []
    if MODEL_CMD:
        command = MODEL_CMD.split() + [prompt]
    elif MODEL_PATH:
        command = ['gpt4all', '-m', MODEL_PATH, '-p', prompt, '--n_predict', '128', '--temp', '0.5']

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        if result.returncode == 0 and result.stdout:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None

    return None


def get_best_faq(message: str, connection: sqlite3.Connection) -> Optional[str]:
    cursor = connection.cursor()
    tokens = [token.strip() for token in re.split(r'[,\s]+', message.lower()) if token]
    candidates = []
    for token in tokens:
        if len(token) < 3:
            continue
        rows = cursor.execute(
            'SELECT question, answer, keywords FROM faqs WHERE lower(keywords) LIKE ? OR lower(question) LIKE ? LIMIT 1',
            (f'%{token}%', f'%{token}%'),
        ).fetchall()
        candidates.extend(rows)

    if candidates:
        return candidates[0][1]

    return None


def search_products(message: str, connection: sqlite3.Connection, limit: int = 3):
    cursor = connection.cursor()
    terms = [term.strip() for term in re.split(r'[^a-zA-Z0-9]+', message.lower()) if term]
    if not terms:
        return []

    query = 'SELECT * FROM products WHERE '
    query += ' OR '.join([f"lower({field}) LIKE ?" for field in SEARCH_FIELDS])
    values = [f'%{term}%' for term in terms for _ in SEARCH_FIELDS]
    rows = cursor.execute(query, values).fetchall()
    products = []
    for row in rows:
        products.append({
            'id': row[0],
            'name': row[1],
            'category': row[2],
            'price': row[3],
            'rating': row[4],
            'tag': row[5],
            'image': row[6],
            'description': row[7],
            'colors': json.loads(row[8] or '[]'),
        })
    unique = []
    seen = set()
    for product in products:
        if product['id'] not in seen:
            seen.add(product['id'])
            unique.append(product)
    return unique[:limit]


def get_order_status(message: str, connection: sqlite3.Connection) -> Optional[str]:
    order_id = None
    match = re.search(r'([A-Za-z0-9-]{6,})', message)
    if match:
        order_id = match.group(1).upper()

    if not order_id:
        return None

    cursor = connection.cursor()
    order = cursor.execute('SELECT id, status, tracking, total, created_at FROM orders WHERE id = ?', (order_id,)).fetchone()
    if not order:
        return None

    return (
        f'Order {order[0]} is currently {order[1]}. Tracking: {order[2]}. Total paid: ${order[3]:.2f}. Placed on {order[4][:10]}.'
    )


def lookup_intent(message: str, connection: sqlite3.Connection) -> Optional[str]:
    cursor = connection.cursor()
    tokens = [token for token in re.split(r'[,\s]+', message.lower()) if token and len(token) > 2]
    if not tokens:
        return None
    rows = cursor.execute('SELECT trigger_keywords, response FROM intents').fetchall()
    for trigger_keywords, response in rows:
        triggers = [keyword.strip() for keyword in trigger_keywords.split(',') if keyword.strip()]
        for trigger in triggers:
            for token in tokens:
                if trigger in token or token in trigger:
                    return response
    return None


def generate_response(message: str, connection: sqlite3.Connection) -> dict:
    message = sanitize_text(message)
    intent = 'default'
    order_status = get_order_status(message, connection)
    if order_status:
        intent = 'order_status'
        return {'response': order_status, 'intent': intent}

    faq_response = get_best_faq(message, connection)
    if faq_response:
        intent = 'faq'
        return {'response': faq_response, 'intent': intent}

    intent_response = lookup_intent(message, connection)
    if intent_response:
        intent = 'intent'
        product_recs = search_products(message, connection)
        response_text = intent_response
        if product_recs:
            response_text += ' Here are a few recommendations:'
            response_text += ' ' + ', '.join([product['name'] for product in product_recs])
        return {'response': response_text, 'intent': intent, 'products': product_recs}

    for keyword, text in RESPONSE_FALLBACK.items():
        if keyword in message.lower():
            intent = f'fallback_{keyword}'
            return {'response': text, 'intent': intent}

    product_recs = search_products(message, connection)
    if product_recs:
        intent = 'product_suggestion'
        return {
            'response': 'I found these products that may match your request.',
            'intent': intent,
            'products': product_recs,
        }

    prompt = (
        'You are an offline ecommerce assistant for a luxury store. Answer the user clearly and concisely using available catalog and policies. ' 
        f'User: {message}\nAssistant:'
    )
    local_model_response = run_local_model(prompt)
    if local_model_response:
        intent = 'local_model'
        return {'response': local_model_response, 'intent': intent}

    return {
        'response': 'I am ready to help with product recommendations, shipping, returns, carts, orders, and support questions. Try asking about a product or your order status.',
        'intent': intent,
    }
