from unittest.mock import MagicMock, patch

import pytest
from kafka.consumer.fetcher import ConsumerRecord
from moderation.ai.models import ClassifyResult
from moderation.kafka.models import KafkaModerationMessage
from moderation.kafka.processor import classify_and_save, process_message


@pytest.fixture
def mock_classify_result():
    return ClassifyResult(
        content_type="image",
        automated_flag=True,
        automated_flag_reason="NSFW detected",
        model_version="test-model/v1",
        analysis_metadata={"nsfw": 0.98},
    )


@pytest.fixture
def image_message():
    return KafkaModerationMessage(
        content_id="123", type="image", filename="test.jpg", filepath="/tmp/test.jpg", message=""
    )


@pytest.fixture
def text_message():
    return KafkaModerationMessage(
        content_id="456", type="text", filename=None, filepath="", message="This is a test message"
    )


@patch("moderation.kafka.processor.get_image_moderation")
@patch("moderation.kafka.processor.save_analysis_result")
def test_classify_and_save_image(mock_save, mock_get_image_mod, image_message, mock_classify_result):
    # Mock classifier
    mock_classifier = MagicMock()
    mock_classifier.classify.return_value = mock_classify_result
    mock_get_image_mod.return_value = mock_classifier

    # Mock save result
    mock_save.return_value = True

    classify_and_save(image_message)

    mock_classifier.classify.assert_called_once_with("/tmp/test.jpg")
    mock_save.assert_called_once()


@patch("moderation.kafka.processor.get_text_classifier")
@patch("moderation.kafka.processor.save_analysis_result")
def test_classify_and_save_text(mock_save, mock_get_text_mod, text_message, mock_classify_result):
    mock_classifier = MagicMock()
    mock_classifier.classify.return_value = mock_classify_result
    mock_get_text_mod.return_value = mock_classifier

    mock_save.return_value = True

    classify_and_save(text_message)

    mock_classifier.classify.assert_called_once_with("This is a test message")
    mock_save.assert_called_once()


@patch("moderation.kafka.processor.classify_and_save")
def test_process_message_valid(mock_classify_save):
    msg_dict = {
        "content_id": "789",
        "type": "text",
        "message": "clean",
        "filename": None,
        "filepath": "",
    }
    record = ConsumerRecord(
        topic="moderation",
        partition=0,
        offset=0,
        timestamp=0,
        timestamp_type=0,
        key=None,
        value=msg_dict,
        checksum=None,
        serialized_key_size=0,
        serialized_value_size=0,
        headers=[],
        leader_epoch=None,
        serialized_header_size=0,
    )

    process_message(record)
    mock_classify_save.assert_called_once()


def test_process_message_invalid():
    # Send in bad data (e.g., missing required fields)
    record = ConsumerRecord(
        topic="moderation",
        partition=0,
        offset=0,
        timestamp=0,
        timestamp_type=0,
        key=None,
        value={"type": "image"},  # Missing fields
        checksum=None,
        serialized_key_size=0,
        serialized_value_size=0,
        headers=[],
        leader_epoch=None,
        serialized_header_size=0,
    )

    # Should not raise exception
    process_message(record)
