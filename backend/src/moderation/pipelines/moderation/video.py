from functools import cache
from typing import Tuple

import numpy as np
from moderation.ai.audio import AudioParser
from moderation.ai.flag import flag_image, flag_text
from moderation.ai.image import ImageClassifier, get_image_classifier
from moderation.ai.text import get_text_classifier
from moderation.parsers.audio import samples_from_video_path
from moderation.parsers.video import frames_with_timestamp_from_video_path
from moderation.pipelines.moderation.aggregators import VideoResultAggregator
from moderation.pipelines.moderation.pipeline import Pipeline, PipelineStage
from moderation.pipelines.moderation.postprocessors import TagResult


@cache
def get_video_pipeline() -> Pipeline:
    video_pipeline = Pipeline(
        extractors=[],
        preprocessors={
            0: [PipelineStage(frames_with_timestamp_from_video_path, "video_to_frames")],
            1: [PipelineStage(samples_from_video_path, "video_to_audio"), PipelineStage(AudioParser().parse, "process_audio")],
        },
        runners={
            0: PipelineStage(VideoRunner(get_image_classifier()), "image_classify_video"),
            1: PipelineStage(get_text_classifier().classify, "text_classify_video"),
        },
        postprocessors={
            0: [
                PipelineStage(flag_image, "flag_image"),
                PipelineStage(TagResult("video"), "tag_result_video"),
            ],
            1: [PipelineStage(flag_text, "flag_image"), PipelineStage(TagResult("video"), "tag_result_video")],
        },
        aggregator={
            0: PipelineStage(VideoResultAggregator(), "video_aggregator"),
        }
    )
    return video_pipeline


class VideoRunner:
    """Thin wrapper to return classification with timestamp"""

    def __init__(self, classifier: ImageClassifier):
        self.classifier = classifier

    def __call__(self, frame_with_timestamp: Tuple[np.ndarray, int]):
        frame, timestamp = frame_with_timestamp
        result = self.classifier.classify(frame)
        result.analysis_metadata["timestamp"] = timestamp
        return result
