import json
import sqlite3
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / 'chatbot.db'

PRODUCT_SEED = [
    {
        'id': 'aura-max',
        'name': 'Aura Max Headphones',
        'category': 'Audio',
        'price': 549,
        'rating': 4.9,
        'tag': 'Signature',
        'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=85',
        'description': 'Studio-grade wireless headphones with spatial audio, soft memory foam, and an all-day battery.',
        'colors': ['Graphite', 'Pearl', 'Silver'],
    },
    {
        'id': 'nova-watch',
        'name': 'Nova Ceramic Watch',
        'category': 'Wearables',
        'price': 799,
        'rating': 4.8,
        'tag': 'New',
        'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1200&q=85',
        'description': 'A polished ceramic smartwatch with health intelligence, crisp display, and refined bands.',
        'colors': ['Porcelain', 'Obsidian', 'Mist'],
    },
    {
        'id': 'halo-lamp',
        'name': 'Halo Ambient Lamp',
        'category': 'Home',
        'price': 320,
        'rating': 4.7,
        'tag': 'Home Edit',
        'image': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1200&q=85',
        'description': 'A sculptural lamp with warm dimming, touch controls, and soft indirect glow.',
        'colors': ['Sandstone', 'Charcoal', 'White'],
    },
    {
        'id': 'monolith-speaker',
        'name': 'Monolith Speaker',
        'category': 'Audio',
        'price': 680,
        'rating': 4.9,
        'tag': 'Best Seller',
        'image': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=1200&q=85',
        'description': 'Room-filling sound in a minimal aluminum body with adaptive room tuning.',
        'colors': ['Black', 'Aluminum'],
    },
    {
        'id': 'arc-sunglasses',
        'name': 'Arc Titanium Sunglasses',
        'category': 'Travel',
        'price': 260,
        'rating': 4.6,
        'tag': 'Limited',
        'image': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=1200&q=85',
        'description': 'Featherweight titanium frames with polarized lenses and a quiet luxury silhouette.',
        'colors': ['Smoke', 'Champagne', 'Black'],
    },
    {
        'id': 'slab-dock',
        'name': 'Slab Charging Dock',
        'category': 'Desk',
        'price': 180,
        'rating': 4.8,
        'tag': 'Essential',
        'image': 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?auto=format&fit=crop&w=1200&q=85',
        'description': 'A machined multi-device dock that keeps your workspace calm, charged, and cable-light.',
        'colors': ['Silver', 'Graphite'],
    },
]

FAQ_SEED = [
    {
        'topic': 'Shipping',
        'question': 'What are the available shipping options?',
        'answer': 'We offer standard shipping, express delivery, and free shipping for orders over $100. Most orders arrive within 3-5 business days.',
        'keywords': 'shipping,delivery,time,cost',
    },
    {
        'topic': 'Refunds',
        'question': 'How do I request a refund?',
        'answer': 'To request a refund, visit the Order section or contact support with your order number. Refunds are processed within 5-7 business days.',
        'keywords': 'refund,return,money back,cancel',
    },
    {
        'topic': 'Payments',
        'question': 'Which payment methods do you accept?',
        'answer': 'We accept credit cards, debit cards, Apple Pay, Google Pay, and secure local checkout options.',
        'keywords': 'payment,credit card,debit card,apple pay,google pay',
    },
    {
        'topic': 'Order Tracking',
        'question': 'How can I track my order?',
        'answer': 'Send us your order ID and we will provide the latest tracking update. Orders typically ship within one business day.',
        'keywords': 'track order,order status,tracking,id',
    },
    {
        'topic': 'Warranty',
        'question': 'What warranty coverage is provided?',
        'answer': 'All products are backed by a one-year limited warranty covering manufacturing defects and quality issues.',
        'keywords': 'warranty,guarantee,guaranteed,coverage',
    },
]

INTENT_SEED = [
    {
        'intent': 'greeting',
        'trigger_keywords': 'hello,hi,hey,welcome,greetings',
        'response': 'Hello! I am your offline shopping assistant. Ask me about products, shipping, orders, or cart updates.',
    },
    {
        'intent': 'product_help',
        'trigger_keywords': 'recommend,find,looking for,show me,best',
        'response': 'I can recommend top products by category, price, or preferences. Try asking for “best audio gifts” or “products under $500.”',
    },
    {
        'intent': 'cart_help',
        'trigger_keywords': 'add to cart,remove from cart,cart summary,show cart,checkout',
        'response': 'I can assist with your cart, add or remove items, and give you a checkout summary whenever you are ready.',
    },
    {
        'intent': 'order_help',
        'trigger_keywords': 'order status,track order,where is my order,delivery status',
        'response': 'Provide your order ID and I will pull the latest status from the offline order database.',
    },
]

ORDER_SEED = [
    {
        'id': 'ORDER-1002',
        'status': 'Shipped',
        'tracking': 'TRACK-88A1',
        'items': json.dumps([{'id': 'aura-max', 'quantity': 1}, {'id': 'halo-lamp', 'quantity': 1}]),
        'total': 869.0,
        'created_at': datetime.utcnow().isoformat(),
    },
    {
        'id': 'ORDER-1003',
        'status': 'Delivered',
        'tracking': 'TRACK-02B3',
        'items': json.dumps([{'id': 'slab-dock', 'quantity': 2}]),
        'total': 360.0,
        'created_at': datetime.utcnow().isoformat(),
    },
]


def initialize_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            rating REAL NOT NULL,
            tag TEXT,
            image TEXT,
            description TEXT,
            colors TEXT
        );
        ''',
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            question TEXT,
            answer TEXT,
            keywords TEXT
        );
        ''',
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS intents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intent TEXT,
            trigger_keywords TEXT,
            response TEXT
        );
        ''',
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            status TEXT,
            tracking TEXT,
            items TEXT,
            total REAL,
            created_at TEXT
        );
        ''',
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            intent TEXT,
            created_at TEXT
        );
        ''',
    )

    existing_products = cursor.execute('SELECT id FROM products').fetchall()
    if not existing_products:
        for product in PRODUCT_SEED:
            cursor.execute(
                'INSERT INTO products (id, name, category, price, rating, tag, image, description, colors) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    product['id'],
                    product['name'],
                    product['category'],
                    product['price'],
                    product['rating'],
                    product['tag'],
                    product['image'],
                    product['description'],
                    json.dumps(product['colors']),
                ),
            )

    existing_faqs = cursor.execute('SELECT id FROM faqs').fetchall()
    if not existing_faqs:
        for faq in FAQ_SEED:
            cursor.execute(
                'INSERT INTO faqs (topic, question, answer, keywords) VALUES (?, ?, ?, ?)',
                (faq['topic'], faq['question'], faq['answer'], faq['keywords']),
            )

    existing_intents = cursor.execute('SELECT id FROM intents').fetchall()
    if not existing_intents:
        for intent in INTENT_SEED:
            cursor.execute(
                'INSERT INTO intents (intent, trigger_keywords, response) VALUES (?, ?, ?)',
                (intent['intent'], intent['trigger_keywords'], intent['response']),
            )

    existing_orders = cursor.execute('SELECT id FROM orders').fetchall()
    if not existing_orders:
        for order in ORDER_SEED:
            cursor.execute(
                'INSERT INTO orders (id, status, tracking, items, total, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                (order['id'], order['status'], order['tracking'], order['items'], order['total'], order['created_at']),
            )

    connection.commit()
    connection.close()


if __name__ == '__main__':
    initialize_database()
    print(f'Initialized database at {DB_PATH}')
