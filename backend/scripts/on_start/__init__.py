from moderation.core.settings import settings
from moderation.on_start.load_clients_to_redis import load_clients_into_redis
from moderation.on_start.load_fixtures import load_fixtures


class OnStart:
    def __init__(self):
        actions = []
        if settings.ENVIRONMENT == "development":
            actions.extend([load_fixtures])
        actions.extend([load_clients_into_redis])
        self.actions = actions

    def run(self):
        for action in self.actions:
            action()


def on_start():
    """Run all actions on start."""
    on_start_actions = OnStart()
    on_start_actions.run()
