from moderation.core.settings import settings
from moderation.models.classification import Result


def flag_image(result: Result) -> Result:
    nsfw = result.analysis_metadata["nsfw"]
    if nsfw > settings.AI_IMAGE_MODERATION_THRESHOLD:
        result.automated_flag = True
        result.automated_flag_reason = f"The result for NSFW content is {nsfw}"
    else:
        result.automated_flag = False
        result.automated_flag_reason = ""


def flag_text(result: Result) -> Result:
    metadata = result.analysis_metadata
    above_threshold = []
    for key, value in metadata.items():
        if value > settings.AI_IMAGE_MODERATION_THRESHOLD:
            above_threshold.append(key)
    if above_threshold:
        result.automated_flag = True
        result.automated_flag_reason = f"The result for toxicity content is {above_threshold}"
    else:
        result.automated_flag = False
        result.automated_flag_reason = ""


def flag_pii(result: Result) -> Result:
    metadata = result.analysis_metadata
    if metadata:
        result.automated_flag = True
        result.automated_flag_reason = f"The result for PII content is {len(metadata)}"
    else:
        result.automated_flag = False
        result.automated_flag_reason = ""
