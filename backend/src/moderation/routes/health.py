def health_check():
    return {"status": "ok"}, 200


def api_version():
    return {"version": "1.0.0"}, 200
