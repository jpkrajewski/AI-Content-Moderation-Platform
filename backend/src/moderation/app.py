from pathlib import Path

import connexion
from moderation.core.container import Container
from moderation.core.settings import settings


def create_app():
    """Create a Flask application."""
    container = Container()
    app = connexion.FlaskApp(__name__, specification_dir=Path(__file__).parent / "spec")
    app.app.container = container
    app.add_api(
        "openapi.yaml",
        base_path="/api/v1",
        strict_validation=True,
        validate_responses=True,
        resolver_error=501,
        auth_all_paths=True,
    )
    print(container.content_service)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=settings.APP_PORT, host=settings.APP_HOST)
