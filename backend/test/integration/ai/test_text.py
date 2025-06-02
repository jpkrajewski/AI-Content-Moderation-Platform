from pathlib import Path

from moderation.ai.text import TextClassifier, get_text_classifier
from pytest import fixture
from moderation.parsers.documents import extract_text_from_document

@fixture
def text_classifier():
    return get_text_classifier()


def test_classify(text_classifier: TextClassifier):
    text = "Hello World, it is perfectly safe message"
    result = text_classifier.classify(text)
    assert result is not None
    assert result.content_type == "text"
    assert isinstance(result.analysis_metadata, dict)
