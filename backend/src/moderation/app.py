from pathlib import Path

import connexion
from moderation.auth.jwt import bearer_auth

app = connexion.App(__name__, specification_dir=Path(__file__).parent)
app.add_api(
    "openapi.yaml",
    base_path="/api/v1",
    strict_validation=True,
    validate_responses=True,
    resolver_error=501,
    auth_all_paths=True,
    security_map={"BearerAuth": bearer_auth},  # <--- important!
)

if __name__ == "__main__":
    app.run(port=8080)
