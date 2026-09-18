
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@auth_bp.route("/ready", methods=["GET"])
def ready():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ready"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"status": "not ready"}), 503


@auth_bp.route("/api/db-check", methods=["GET"])
def db_check():
    try:
        User.query.limit(1).all()
        return jsonify({
            "database": "connected",
            "users_table": "available"
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"database": "error"}), 503


@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    email = data.get("email")

    if not isinstance(email, str) or not email.strip():
        return jsonify({"error": "A valid email is required"}), 400

    email = email.strip().lower()

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409

    user = User(email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered",
        "user_id": user.id
    }), 201