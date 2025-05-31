from functools import cache

from moderation.pipelines.moderation.audio import get_audio_pipeline
from moderation.pipelines.moderation.documents import get_document_pipeline
from moderation.pipelines.moderation.enums import PipelineType
from moderation.pipelines.moderation.image import get_image_pipeline
from moderation.pipelines.moderation.pipeline import Pipeline
from moderation.pipelines.moderation.text import get_text_pipeline
from moderation.pipelines.moderation.video import get_video_pipeline


@cache
def get_pipeline(pipeline_type: PipelineType) -> Pipeline:
    pipelines = {
        PipelineType.IMAGE: get_image_pipeline(),
        PipelineType.TEXT: get_text_pipeline(),
        PipelineType.DOCUMENT: get_document_pipeline(),
        PipelineType.VIDEO: get_video_pipeline(),
        PipelineType.AUDIO: get_audio_pipeline(),
    }
    return pipelines[pipeline_type]
