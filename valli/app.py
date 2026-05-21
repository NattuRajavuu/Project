import logging
import os
from datetime import timedelta

from flask import Flask, render_template, session
from flask_cors import CORS

from routes.auth_routes import auth_bp
from routes.chatbot_routes import chatbot_bp
from routes.product_routes import product_bp
from utils.helpers import cart_count, load_products, money


try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as env_file:
            for line in env_file:
                if "=" in line and not line.lstrip().startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ.setdefault(key, value)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=14)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    app.register_blueprint(product_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chatbot_bp)

    @app.context_processor
    def inject_globals():
        return {
            "cart_count": cart_count(),
            "wishlist_count": len(session.get("wishlist", [])),
            "current_user": session.get("user"),
            "money": money,
        }

    @app.get("/")
    def home():
        products = load_products()
        return render_template(
            "home.html",
            products=products,
            featured=products[:3],
            testimonials=[
                "The calmest shopping experience I have used this year.",
                "The AI assistant helped me choose a gift in under a minute.",
                "Beautiful product pages, fast checkout, and excellent curation.",
            ],
        )

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("base.html", error_message="Page not found"), 404

    @app.errorhandler(500)
    def server_error(error):
        app.logger.exception("Unhandled server error: %s", error)
        return render_template("base.html", error_message="Something went wrong."), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1", host="127.0.0.1", port=8000)
