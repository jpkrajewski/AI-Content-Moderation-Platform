from functools import cache

from moderation.ai.flag import flag_image
from moderation.ai.image import get_image_classifier
from moderation.pipelines.pipeline import Pipeline, PipelineStage
from moderation.pipelines.preprocessors import ImageFromPath


@cache
def get_image_pipeline() -> Pipeline:
    image_pipeline = Pipeline(
        extractors=[],
        preprocessors={0: [PipelineStage(ImageFromPath(), "PILImage_from_path")]},
        runners={0: PipelineStage(get_image_classifier().classify, "image_classify")},
        postprocessors={
            0: [PipelineStage(flag_image, "flag_image")],
        },
    )
    return image_pipeline
