from pathlib import Path

from moderation.ai.text import TextModeration, get_text_classifier
from pytest import fixture

IMAGES_FOLDER_PATH = Path(__name__).cwd() / "test" / "unit" / "ai"


@fixture
def image_classifier():
    return get_text_classifier()


def test_classify_pdf(image_classifier: TextModeration):
    result = image_classifier.classify_from_document(str(IMAGES_FOLDER_PATH / "file-example_PDF_1MB.pdf"))
    assert result is not None
    assert result.content_type == "document"
    assert result.automated_flag is False
    assert result.automated_flag_reason == ""
    assert isinstance(result.analysis_metadata, dict)


def test_classify_docx(image_classifier: TextModeration):
    result = image_classifier.classify_from_document(str(IMAGES_FOLDER_PATH / "example.docx"))
    assert result is not None
    assert result.content_type == "document"
    assert result.automated_flag is False
    assert result.automated_flag_reason == ""
    assert isinstance(result.analysis_metadata, dict)
