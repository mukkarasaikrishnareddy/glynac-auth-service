
from flask import Flask
from app import models

from app.config import get_config
from app.extensions import db, migrate
from app.routes import auth_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(get_config())

    # Initialize database extensions
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)

    return app