from dependency_injector.wiring import Provide, inject
from moderation.core.container import Container
from moderation.service.summary import SummaryService


# @cached_response(DASHBOARD_SUMMARY)
@inject
def get_summary(
    summary_service: SummaryService = Provide[Container.summary_service],
):

    return summary_service.get_dashboard_summary(), 200


def get_user_activity():
    return {"message": "User activity metrics mock"}, 200


def get_moderation_stats():
    return {"message": "Moderation KPIs mock"}, 200
