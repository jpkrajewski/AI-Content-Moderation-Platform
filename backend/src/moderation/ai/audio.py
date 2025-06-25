from functools import cache

from transformers import pipeline
from moderation.core.settings import settings



class AudioParser:
    def __init__(self):
        self.asr_pipeline = pipeline(
            task="automatic-speech-recognition",
            model=settings.AI_AUDIO_MODEL_PATH,
            tokenizer=settings.AI_AUDIO_MODEL_PATH,
            feature_extractor=settings.AI_AUDIO_MODEL_PATH,
        )

    def parse(self, audio_file: str) -> str:
        return self.asr_pipeline(audio_file, return_timestamps=True)["text"]

@cache
def get_audio_parser() -> AudioParser:
    return AudioParser()


