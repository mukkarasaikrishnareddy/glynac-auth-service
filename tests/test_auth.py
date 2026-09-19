
import pytest

from app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture
def client():
    app = create_app()

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://",
    )

    with app.app_context():
        db.create_all()

        user = User(email="test@example.com")
        user.set_password("TestPass123!")

        db.session.add(user)
        db.session.commit()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()


# -------------------------
# Login tests
# -------------------------

def test_login_success(client):
    response = client.post(
        "/api/login",
        json={
            "email": "test@example.com",
            "password": "TestPass123!",
        },
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Login successful"


def test_login_wrong_password(client):
    response = client.post(
        "/api/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid email or password"


def test_login_missing_credentials(client):
    response = client.post(
        "/api/login",
        json={"email": "test@example.com"},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Email and password are required"


# -------------------------
# Registration tests
# -------------------------

def test_register_success(client):
    response = client.post(
        "/api/register",
        json={
            "email": "newuser@example.com",
            "password": "NewPass123!",
        },
    )

    assert response.status_code == 201

    user = User.query.filter_by(
        email="newuser@example.com"
    ).first()

    assert user is not None
    assert user.check_password("NewPass123!")


def test_register_duplicate_email(client):
    response = client.post(
        "/api/register",
        json={
            "email": "test@example.com",
            "password": "AnotherPass123!",
        },
    )

    assert response.status_code == 409
    assert response.get_json()["error"] == "Email already registered"


def test_register_missing_credentials(client):
    response = client.post(
        "/api/register",
        json={"email": "newuser@example.com"},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Email and password are required"