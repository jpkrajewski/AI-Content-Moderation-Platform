import logging
import logging.config
from pathlib import Path

from connexion import FlaskApp
from connexion.middleware import MiddlewarePosition
from moderation.core.container import Container
from moderation.core.settings import settings
from moderation.middlewares.cors import CORSMiddleware


def setup_logging():
    logging.config.fileConfig(
        settings.LOGGER_CONF_PATH,
        disable_existing_loggers=False,
    )


def add_middleware(app: FlaskApp) -> None:
    app.add_middleware(
        CORSMiddleware,
        position=MiddlewarePosition.BEFORE_ROUTING,
        allow_origins=["*"],
        allow_credentials=True,
    )


def add_routes(app: FlaskApp) -> None:
    app.add_api(
        "openapi.yaml",
        base_path="/api/v1",
        strict_validation=True,
        validate_responses=True,
        resolver_error=501,
        auth_all_paths=True,
    )


def add_container(app: FlaskApp) -> None:
    app.app.container = Container()


def create_app():
    setup_logging()
    app = FlaskApp(__name__, specification_dir=Path(__file__).parent / "spec")
    add_container(app)
    add_routes(app)
    add_middleware(app)
    return app
