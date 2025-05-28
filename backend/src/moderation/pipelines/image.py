from moderation.ai.image import get_image_classifier
from moderation.ai.pii import get_pii_analyzer
from moderation.ai.text import get_text_classifier
from moderation.parsers.documents import extract_text_from_document
from moderation.parsers.urls import extract_urls
from moderation.pipelines.pipeline import Pipeline, PipelineStage
from moderation.validators.urls import AsyncGoogleSafeBrowsingClient

image_pipeline = Pipeline(
    extractors=[],  # no extract step needed
    preprocessors={},  # no preprocessing
    runners={
        0: PipelineStage(get_image_classifier().classify, "image_classify")
    }
)
