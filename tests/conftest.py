import pytest

from app import create_app
from app.db import db


@pytest.fixture(scope="session")
def app():
    """Create a Flask app configured for testing."""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="function")
def db_session(app):
    """Provide a database session for a test."""
    with app.app_context():
        session = db.session
        yield session
        session.rollback()
        session.remove()
