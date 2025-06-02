from pathlib import Path

from moderation.ai.audio import get_audio_parser



def test_audio_parser(test_folder):
    parser = get_audio_parser()
    result = parser.parse(str(test_folder / "what-genius-movie-spoken.wav"))
    assert result