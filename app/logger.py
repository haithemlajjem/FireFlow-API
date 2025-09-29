from logging.config import dictConfig


def configure_logging(app):
    """Configure structured logging for Flask."""
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
            "detailed": {
                "format": '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }

    dictConfig(log_config)
    app.logger.info("Logging configured")
