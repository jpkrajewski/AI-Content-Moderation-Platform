from moderation.ai.models import Result
from moderation.core.settings import settings

def flag_image(result: Result) -> Result:
    nsfw = result.analysis_metadata["nsfw"]
    if nsfw > settings.AI_IMAGE_MODERATION_THRESHOLD:
        result.automated_flag = True
        result.automated_flag_reason = f"The result for NSFW content is {nsfw}"


def flag_text(result: Result) -> Result:
    metadata = result.analysis_metadata
    above_treshold = []
    for key, value in metadata.items():
        if value > settings.AI_IMAGE_MODERATION_THRESHOLD:
            above_treshold.append(key)
    if above_treshold:
        result.automated_flag = True
        result.automated_flag_reason = f"The result for toxicity content is {above_treshold}"


def flag_pii(result: Result) -> Result:
    metadata = result.analysis_metadata
    if metadata:
        result.automated_flag = True
        result.automated_flag_reason = f"The result for PII content is {len(metadata)}"