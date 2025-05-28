from moderation.ai.flag import flag_image
from moderation.ai.image import get_image_classifier
from moderation.pipelines.pipeline import Pipeline, PipelineStage

image_pipeline = Pipeline(
    extractors=[],  # no extract step needed
    preprocessors={},  # no preprocessing
    runners={0: PipelineStage(get_image_classifier().classify, "image_classify")},
    postprocessors={
        0: PipelineStage(flag_image, "flag_image"),
    },
)
