from pathlib import Path

from moderation.ai.image import ImageClassifier, get_image_classifier
from pytest import fixture

IMAGES_FOLDER_PATH = Path(__file__).parent


@fixture
def image_classifier():
    return get_image_classifier()


def test_classify_jpg(image_classifier: ImageClassifier):
    result = image_classifier.classify(str(IMAGES_FOLDER_PATH / "cat.jpg"))
    assert result is not None
    assert result.content_type == "image"
    assert isinstance(result.analysis_metadata, dict)
    assert "normal" in result.analysis_metadata
    assert "nsfw" in result.analysis_metadata


def test_classify_png(image_classifier: ImageClassifier):
    result = image_classifier.classify(str(IMAGES_FOLDER_PATH / "diagram.png"))
    assert result is not None
    assert result.content_type == "image"
    assert isinstance(result.analysis_metadata, dict)
    assert "normal" in result.analysis_metadata
    assert "nsfw" in result.analysis_metadata
