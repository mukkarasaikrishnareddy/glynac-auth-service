
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

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Check required fields first
    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    # Then validate password length
    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters"
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "error": "Email already registered"
        }), 409

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }), 201

@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }), 200