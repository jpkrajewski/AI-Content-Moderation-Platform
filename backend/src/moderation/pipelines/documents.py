from functools import cache

from moderation.ai.flag import flag_pii, flag_text
from moderation.ai.pii import get_pii_analyzer
from moderation.ai.text import get_text_classifier
from moderation.parsers.documents import extract_text_from_document
from moderation.parsers.urls import extract_urls
from moderation.pipelines.pipeline import Pipeline, PipelineStage
from moderation.pipelines.postprocessors import ResultExcludeEmpty, TagResult
from moderation.validators.flag import flag_url
from moderation.validators.urls import AsyncGoogleSafeBrowsingClient


@cache
def get_document_pipeline() -> Pipeline:
    document_pipeline = Pipeline(
        extractors=[PipelineStage(extract_text_from_document, "extract_text")],
        preprocessors={2: [PipelineStage(extract_urls, "extract_urls")]},
        runners={
            0: PipelineStage(get_text_classifier().classify, "text_classify"),
            1: PipelineStage(get_pii_analyzer().analyze, "pii_analyze"),
            2: PipelineStage(AsyncGoogleSafeBrowsingClient().check_urls, "safe_browsing_check"),
        },
        postprocessors={
            0: [PipelineStage(flag_text, "flag_result"), PipelineStage(TagResult("document"), "tag_result")],
            1: [
                PipelineStage(flag_pii, "flag_result"),
                PipelineStage(TagResult("document"), "tag_result"),
                PipelineStage(ResultExcludeEmpty(), "exclude_empty_pii_result"),
            ],
            2: [
                PipelineStage(flag_url, "flag_result"),
                PipelineStage(TagResult("document"), "tag_result"),
                PipelineStage(ResultExcludeEmpty(), "exclude_empty_url_result"),
            ],
        },
    )
    return document_pipeline
