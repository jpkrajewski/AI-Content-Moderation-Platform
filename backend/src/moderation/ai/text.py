from functools import cache

import torch
from moderation.core.settings import settings
from moderation.models.classification import Result
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class TextClassifier:
    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(
            settings.AI_TEXT_MODEL_PATH, local_files_only=True
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            settings.AI_TEXT_MODEL_PATH, local_files_only=True
        )

    def classify(self, text: str) -> Result:
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
        return Result(
            content_type="text",
            model_version=settings.AI_TEXT_MODEL_PATH,
            analysis_metadata={labels[i]: score.item() for i, score in enumerate(probs[0])},
        )


@cache
def get_text_classifier() -> TextClassifier:
    return TextClassifier()
