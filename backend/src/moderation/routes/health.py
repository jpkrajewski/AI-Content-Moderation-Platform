from moderation import MODERATION_VERSION


def health_check():
    return {"status": "ok"}, 200


def api_version():
    return {"version": MODERATION_VERSION}, 200
