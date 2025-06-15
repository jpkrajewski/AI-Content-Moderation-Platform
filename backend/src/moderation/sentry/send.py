import sentry_sdk
from sentry_sdk import capture_exception


def send_exception_to_sentry(
        e: Exception,
        extra_info: dict = None,
        tags: dict = None,
) -> None:
    """
    Send an exception to Sentry with optional extra data and tags.

    Args:
        e (Exception): The exception to send to Sentry.
        extra_info (dict, optional): A dictionary of extra information to add to the event. Defaults to None.
        tags (dict, optional): A dictionary of tags to add to the event. Defaults to None.
    """
    scope = sentry_sdk.get_current_scope()
    if extra_info:
        for key, value in extra_info.items():
            scope.set_extra(key, value)

    if tags:
        for key, value in tags.items():
            scope.set_tag(key, value)
    capture_exception(e)
