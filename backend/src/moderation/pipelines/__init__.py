from moderation.pipelines.documents import document_pipeline
from moderation.pipelines.text import text_pipeline
from moderation.pipelines.documents import document_pipeline
from moderation.pipelines.image import image_pipeline
from moderation.pipelines.enums import PipelineType
from moderation.pipelines.pipeline import Pipeline

def get_pipeline(pipeline_type: PipelineType) -> Pipeline:
    pipelines = {
        PipelineType.IMAGE: image_pipeline,
        PipelineType.TEXT: text_pipeline,
        PipelineType.DOCUMENT: document_pipeline,
    }
    return pipelines[pipeline_type]