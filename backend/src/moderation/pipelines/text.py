from moderation.ai.pii import get_pii_analyzer
from moderation.ai.text import get_text_classifier
from moderation.ai.flag import flag_text, flag_pii
from moderation.parsers.documents import extract_text_from_document
from moderation.parsers.urls import extract_urls
from moderation.pipelines.pipeline import Pipeline, PipelineStage
from moderation.validators.urls import AsyncGoogleSafeBrowsingClient

text_pipeline = Pipeline(
    extractors=[],  # raw text is input
    preprocessors={},  # no preprocessing
    runners={
        0: PipelineStage(get_text_classifier().classify, "text_classify"),
        1: PipelineStage(get_pii_analyzer().analyze, "pii_analyze"),
        2: PipelineStage(AsyncGoogleSafeBrowsingClient().check_urls, "safe_browsing_check"),
    },
    postprocess={
        0: PipelineStage(flag_text, "flag_result"),
        1: PipelineStage(flag_pii, "flag_result"),
    }
)