import os

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

# Blueprints
from app.api.firewalls import bp as firewalls_bp
from app.api.policies import bp as policies_bp
from app.api.rules import bp as rules_bp
from app.db import init_db
from app.logger import configure_logging

# Import definitions
from app.schemas.firewall import definitions as firewall_definitions
from app.schemas.policy import definitions as policy_definitions
from app.schemas.rule import definitions as rule_definitions


def create_app(test_config=None):
    """Flask app factory with Flasgger Swagger docs enabled and structured logging."""
    app = Flask(__name__)

    default_sqlite = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///fireflow.db")
    app.config.from_mapping({"SQLALCHEMY_DATABASE_URI": default_sqlite})

    if test_config:
        app.config.update(test_config)

    # Logging
    configure_logging(app)

    # Database
    init_db(app)

    # CORS
    CORS(app)

    # Register Blueprints
    app.register_blueprint(firewalls_bp)
    app.register_blueprint(policies_bp)
    app.register_blueprint(rules_bp)

    # Swagger
    swagger = Swagger(app)
    swagger.template = {
        "swagger": "2.0",
        "info": {
            "title": "FireFlow API",
            "description": "API for managing firewalls, policies, and rules",
            "version": "1.0.0",
        },
        "definitions": {
            **firewall_definitions,
            **policy_definitions,
            **rule_definitions,
        },
    }

    @app.route("/")
    def index():
        app.logger.info("Root endpoint accessed")
        return {"message": "FireFlow API", "docs": "/apidocs"}

    return app
