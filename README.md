# Glynac Auth Service — CI/CD Demo

A personal learning project to build a containerized authentication service and progressively implement a secure CI/CD workflow with environment-specific deployment configuration.

> **Project status:** Development in progress. This is a demo scaffold using Flask and SQLite. It is not connected to any organization's infrastructure.

## Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Migrate / Alembic
* SQLite (local development)
* Docker
* Pytest

## Current Features

* Flask application factory
* Environment-based configuration for development, staging, and production
* Health endpoint: `GET /health`
* Readiness endpoint with database connectivity check: `GET /ready`
* Database check endpoint: `GET /api/db-check`
* User registration endpoint: `POST /api/register`
* SQLAlchemy `User` model with unique email addresses
* Database migrations initialized and applied
* Duplicate registration returns HTTP `409 Conflict`
* Basic health and readiness tests

## API Endpoints

| Method | Endpoint        | Purpose                                      |
| ------ | --------------- | -------------------------------------------- |
| GET    | `/health`       | Checks whether the application responds      |
| GET    | `/ready`        | Checks database connectivity                 |
| GET    | `/api/db-check` | Checks whether the users table is accessible |
| POST   | `/api/register` | Registers a user using an email              |

### Registration example

Request:

```json
{
  "email": "demo@example.com"
}
```

Successful registration returns HTTP `201 Created`. Registering the same email again returns HTTP `409 Conflict`.

## Local Setup

### 1. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 2. Run database migrations

```powershell
python -m flask --app run.py db upgrade
```

### 3. Start the application

```powershell
python run.py
```

The application runs locally on port `5000`.

## Run Tests

```powershell
python -m pytest -v
```

## Docker

Build the image:

```powershell
docker build -t glynac-auth-service:dev .
```

Run the container:

```powershell
docker run --rm -p 5000:5000 glynac-auth-service:dev
```

## Environment Plan

Planned demo environments:

* **dev**
* **staging**
* **prod**

Planned environment-specific configuration includes Nomad addresses and namespaces, Vault secret prefixes, and deployment credentials. These are project targets only; no organization infrastructure or credentials are configured.

## Security and Development Notes

* Password hashing and login are **not implemented yet**.
* The current registration endpoint stores email only.
* The local fallback secret is for development only.
* Do not commit real secrets, passwords, tokens, or `.env` files.
* Production database integration, authentication, authorization, rate limiting, and deployment protections remain future work.

## Next Steps

1. Add password hashing to the user model and registration flow.
2. Add input validation and authentication tests.
3. Implement login and token handling.
4. Review error handling and security controls.
5. Continue Docker and CI/CD setup.
6. Plan environment-specific deployment configuration.
