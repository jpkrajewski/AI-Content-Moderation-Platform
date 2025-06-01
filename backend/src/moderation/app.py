import logging
import logging.config
from pathlib import Path
from authlib.integrations.flask_client import OAuth
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

def add_oauth(app: FlaskApp) -> None:
    container: Container = app.app.container
    oauth = container.oauth()
    oauth.init_and_register_app(app.app)


def add_container(app: FlaskApp) -> None:
    app.app.container = Container()

def configure_session(app: FlaskApp) -> None:
    app.app.secret_key = settings.APP_SECRET_KEY


def create_app():
    setup_logging()
    app = FlaskApp(__name__, specification_dir=Path(__file__).parent / "spec")
    configure_session(app)
    add_container(app)
    add_oauth(app)
    add_routes(app)
    add_middleware(app)
    return app
