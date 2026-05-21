from flask import Flask, jsonify
from flask_cors import CORS

try:
    from routes.chat import chat_bp
    from routes.products import products_bp
except ModuleNotFoundError:
    from backend.routes.chat import chat_bp
    from backend.routes.products import products_bp


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(products_bp, url_prefix="/api")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "online", "mode": "offline-first"})

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Endpoint not found"}), 404

    return app


app = create_app()


if __name__ == "__main__":
    print("Luxe offline commerce API running at http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
