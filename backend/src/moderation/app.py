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
    logger = logging.getLogger("moderation")
    logger.info("Logging is set up.")
    logger.debug("This is a debug message from moderation.")
    logger.info("This is an info message from moderation.")
    logger.error("This is an error message from moderation.")


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
    print("loas...")
    app.app.container = Container()


def create_app():
    setup_logging()
    app = FlaskApp(__name__, specification_dir=Path(__file__).parent / "spec")
    add_container(app)
    add_routes(app)
    add_middleware(app)
    return app
