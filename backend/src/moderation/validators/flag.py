from moderation.models.classification import Result


def flag_url(result: Result):
    count = 0
    for metadata in result.analysis_metadata["results"]:
        if not metadata.get("safe"):
            count += 1
    if count > 1:
        result.automated_flag = True
        result.automated_flag_reason = f"The text is containing {count} unsafe urls"
    else:
        result.automated_flag = False
        result.automated_flag_reason = ""
    return result
