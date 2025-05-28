from functools import cache

from moderation.pipelines.documents import get_document_pipeline
from moderation.pipelines.enums import PipelineType
from moderation.pipelines.image import get_image_pipeline
from moderation.pipelines.pipeline import Pipeline
from moderation.pipelines.text import get_text_pipeline


@cache
def get_pipeline(pipeline_type: PipelineType) -> Pipeline:
    pipelines = {
        PipelineType.IMAGE: get_image_pipeline(),
        PipelineType.TEXT: get_text_pipeline(),
        PipelineType.DOCUMENT: get_document_pipeline(),
    }
    return pipelines[pipeline_type]
