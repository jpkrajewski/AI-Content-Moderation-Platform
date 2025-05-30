from pathlib import Path

from PIL.Image import Image

from moderation.ai.image import ImageClassifier, get_image_classifier
from pytest import fixture



@fixture
def image_classifier():
    return get_image_classifier()


def test_classify_jpg(test_folder, image_classifier: ImageClassifier):
    result = image_classifier.classify(Image.open(str(test_folder / "cat.jpg")).convert("RGB"))
    assert result is not None
    assert result.content_type == "image"
    assert isinstance(result.analysis_metadata, dict)
    assert "normal" in result.analysis_metadata
    assert "nsfw" in result.analysis_metadata


def test_classify_png(image_classifier: ImageClassifier):
    result = image_classifier.classify(Image.open(test_folder / "diagram.png"))
    assert result is not None
    assert result.content_type == "image"
    assert isinstance(result.analysis_metadata, dict)
    assert "normal" in result.analysis_metadata
    assert "nsfw" in result.analysis_metadata
