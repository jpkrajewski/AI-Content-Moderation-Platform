from functools import cache

from transformers import pipeline
from moderation.core.settings import settings



class AudioParser:
    def __init__(self):
        self.asr_pipeline = pipeline("automatic-speech-recognition", model=settings.AI_AUDIO_MODEL)

    def parse(self, audio_file: str) -> str:
        return self.asr_pipeline(audio_file, return_timestamps=True)["text"]

@cache
def get_audio_parser() -> AudioParser:
    return AudioParser()


