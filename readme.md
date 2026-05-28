# Tiza Server

A Flask-based backend API for an equipment rental marketplace. The server supports user authentication, email verification, listings management, categories, and PostgreSQL-backed persistence.

## Key Features

- JWT authentication with access and refresh tokens
- Email verification for new user registration
- Listings CRUD operations with validation
- Category management and pagination support
- Modular Flask app using blueprints
- Database migrations with Flask-Migrate and Alembic
- Email integration via Flask-Mail

## Tech Stack

- Python 3
- Flask
- Flask-JWT-Extended
- Flask-Mail
- Flask-Migrate
- Flask-SQLAlchemy
- Marshmallow
- PostgreSQL

## Getting Started

1. Create and activate a Python environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and configure the environment variables:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
JWT_TOKEN_LOCATION=headers
JWT_REFRESH_COOKIE_NAME=refresh_token
JWT_COOKIE_SECURE=False
JWT_COOKIE_SAMESITE=Lax
JWT_COOKIE_CSRF_PROTECT=True
EMAIL_VERIFICATION_SALT=your-email-salt
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
MAIL_DEFAULT_SENDER=Your App <no-reply@example.com>
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost:5432/tiza_db
PORT=4500
FLASK_DEBUG=True
```

4. Initialize and apply database migrations:

```bash
flask db upgrade
```

5. Run the server:

```bash
python run.py
```

## Project Structure

- `app.py` — Flask application factory and blueprint registration
- `run.py` — Application entrypoint
- `config.py` — Environment-based configuration
- `auth/`, `users/`, `listings/`, `categories/` — Domain modules
- `db/` — Database models and migrations
- `utils/` — Shared utilities for responses, email, validation

## Notes

- Ensure your email and database credentials are correct in `.env`.
- The email verification flow relies on `verify_email` templates in `templates/email-templates/`.
- The refresh token is stored in a secure cookie and access tokens are returned in the response body.

## License

Add your preferred license information here.
