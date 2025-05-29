from functools import cache

from transformers import pipeline




class AudioParser:
    def __init__(self):
        self.asr_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-small")

    def parse(self, audio_file: str) -> str:
        return self.asr_pipeline(audio_file, return_timestamps=True)["text"]

@cache
def get_audio_parser() -> AudioParser:
    return AudioParser()


