from flask import Flask

from auth.routes import auth_bp
from models.db import init_app
from routes.main import main_bp
from routes.quiz import quiz_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "replace-this-secret-key-before-deployment"
    app.config["DATABASE"] = "database/database.db"

    init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
