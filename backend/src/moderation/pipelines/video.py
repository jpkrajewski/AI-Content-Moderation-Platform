import asyncio
from functools import cache

from moderation.ai.flag import flag_image
from moderation.ai.image import get_image_classifier
from moderation.ai.text import get_text_classifier
from moderation.pipelines.pipeline import Pipeline, PipelineStage
from moderation.pipelines.preprocessors import ImageFromPath, VideoToAudio, VideoToFrames
from moderation.ai.audio import AudioParser


@cache
def get_video_pipeline() -> Pipeline:
    video_pipeline = Pipeline(
        extractors=[],
        preprocessors={0: [PipelineStage(VideoToFrames(), "video_to_frames")],
                       1: [PipelineStage(VideoToAudio(), "video_to_audio"), PipelineStage(AudioParser().parse, "process_audio")]},
        runners={
            0: PipelineStage(get_image_classifier().classify, "image_classify"),
            1: PipelineStage(get_text_classifier().classify, "text_classify")
        },
        postprocessors={},
    )
    return video_pipeline

