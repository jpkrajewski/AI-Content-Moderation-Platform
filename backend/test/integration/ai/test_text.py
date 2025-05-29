from pathlib import Path

from moderation.ai.text import TextClassifier, get_text_classifier
from pytest import fixture
from moderation.parsers.documents import extract_text_from_document

IMAGES_FOLDER_PATH = Path(__file__).parent

@fixture
def image_classifier():
    return get_text_classifier()


def test_classify_pdf(image_classifier: TextClassifier):
    text = extract_text_from_document(str(IMAGES_FOLDER_PATH / "file-example_PDF_1MB.pdf"))
    result = image_classifier.classify(text)
    assert result is not None
    assert result.content_type == "text"
    assert isinstance(result.analysis_metadata, dict)


def test_classify_docx(image_classifier: TextClassifier):
    text = extract_text_from_document(str(IMAGES_FOLDER_PATH / "example.docx"))
    result = image_classifier.classify(text)
    assert result is not None
    assert result.content_type == "text"
    assert isinstance(result.analysis_metadata, dict)
