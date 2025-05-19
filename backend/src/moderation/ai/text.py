from abc import ABC, abstractmethod
from functools import cache

from moderation.ai.models import ClassifyResult
from moderation.core.settings import settings

try:
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
except ImportError:
    if not settings.AI_USE_MOCK:
        raise ImportError(
            "The required libraries for image moderation are not installed. "
            "Please install the necessary libraries or set AI_USE_MOCK to True."
        )


class TextClassifier(ABC):
    @abstractmethod
    def classify(self, text: str) -> ClassifyResult: ...


class TextModeration(TextClassifier):
    def __init__(self) -> None:
        self.tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained(settings.AI_TEXT_MODERATION_MODEL)
        self.model: AutoModelForSequenceClassification = AutoModelForSequenceClassification.from_pretrained(
            settings.AI_TEXT_MODERATION_MODEL
        )

    def classify(self, text: str) -> ClassifyResult:
        """
        Moderates text using a pre-trained model.
        Args:
            text (str): The text to be moderated.
        Returns:
            dict: A dictionary with class labels and their corresponding probabilities.
        Example:
            >>> text_moderation = TextModeration()
            >>> results = text_moderation.moderate_text("You are the worst person ever.")
            >>> print(results)
            {
                'toxic': 0.9650261998176575,
                'severe_toxic': 0.006256538443267345,
                'obscene': 0.15708576142787933,
                'threat': 0.00156571960542351,
                'insult': 0.815239667892456,
                'identity_hate': 0.005933417472988367
            }
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        outputs = self.model(**inputs)
        probs = torch.sigmoid(outputs.logits)
        labels = self.model.config.id2label
        flagged = bool(probs[0][0] > settings.AI_TEXT_MODERATION_THRESHOLD)
        flagged_reason = "Toxic content detected" if flagged else ""
        return ClassifyResult(
            content_type="text",
            automated_flag=flagged,
            automated_flag_reason=flagged_reason,
            model_version=settings.AI_TEXT_MODERATION_MODEL,
            analysis_metadata={labels[i]: score.item() for i, score in enumerate(probs[0])},
        )


class TextModerationFake(TextClassifier):
    def classify(self, text: str) -> ClassifyResult:
        return ClassifyResult(
            content_type="text",
            automated_flag=False,
            automated_flag_reason="",
            model_version="fake_model",
            analysis_metadata={},
        )


@cache
def get_text_moderation() -> TextClassifier:
    """
    Factory function to get the text moderation instance.
    Returns:
        TextModeration: An instance of the TextModeration class.
    """
    if settings.AI_USE_MOCK:
        return TextModerationFake()
    return TextModeration()
