from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    with app.app_context():
        db.create_all()


def get_db():
    """Return the current SQLAlchemy session."""
    return db.session
