
from flask import Flask

from app.config import get_config
from app.extensions import db, migrate
from app.routes import auth_bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(get_config())

    # Apply test overrides before initializing SQLAlchemy.
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app import models

    migrate.init_app(app, db)
    app.register_blueprint(auth_bp)

    return app