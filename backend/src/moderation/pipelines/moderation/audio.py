from functools import cache

from moderation.ai.audio import AudioParser
from moderation.ai.flag import flag_text
from moderation.ai.text import get_text_classifier
from moderation.parsers.audio import samples_from_video_path
from moderation.pipelines.moderation.pipeline import Pipeline, PipelineStage
from moderation.pipelines.moderation.postprocessors import TagResult


@cache
def get_audio_pipeline() -> Pipeline:
    audio_pipeline = Pipeline(
        extractors=[],
        preprocessors={
            0: [PipelineStage(samples_from_video_path, "load_audio"), PipelineStage(AudioParser().parse, "audio_to_text")]
        },
        runners={
            0: PipelineStage(get_text_classifier().classify, "text_classify_audio"),
        },
        postprocessors={
            0: [PipelineStage(flag_text, "flag_text"), PipelineStage(TagResult("audio"), "tag_result_audio")]
        },
    )
    return audio_pipeline
