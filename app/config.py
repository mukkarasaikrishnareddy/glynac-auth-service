
import os


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "local-demo-secret-change-me"
    )

    # Flask-SQLAlchemy requires this exact setting name
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///auth.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False


def get_config():
    environment = os.getenv("APP_ENV", "development").lower()

    configs = {
        "development": DevelopmentConfig,
        "staging": StagingConfig,
        "production": ProductionConfig,
    }

    return configs.get(environment, DevelopmentConfig)