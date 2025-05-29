from pathlib import Path

from moderation.ai.audio import get_audio_parser


FOLDER = Path(__file__).parent

def test_audio_parser():
    parser = get_audio_parser()
    result = parser.parse(str(FOLDER / "what-genius-movie-spoken.wav"))
    assert result["text"]