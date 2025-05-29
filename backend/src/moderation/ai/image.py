from functools import cache

import numpy as np
import torch
from moderation.core.settings import settings
from moderation.models.classification import Result
from PIL import Image
from transformers import AutoFeatureExtractor, AutoModelForImageClassification


class ImageClassifier:
    def __init__(self) -> None:

        self.extractor: AutoFeatureExtractor = AutoFeatureExtractor.from_pretrained(settings.AI_IMAGE_MODERATION_MODEL)
        self.model: AutoModelForImageClassification = AutoModelForImageClassification.from_pretrained(
            settings.AI_IMAGE_MODERATION_MODEL
        )

    def classify(self, image: Image) -> Result:
        """
        Example:
            >>> image_moderation = ImageModeration()
            >>> results = image_moderation.moderate_image("path/to/image.jpg")
            >>> print(results)
            {'normal': 0.95, 'nsfw': 0.05}
        """
        inputs = self.extractor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

        # Map class indices to labels
        labels = self.model.config.id2label
        analysis_metadata = {labels[idx]: score.item() for idx, score in enumerate(probs[0])}
        return Result(
            content_type="image",
            model_version=settings.AI_IMAGE_MODERATION_MODEL,
            analysis_metadata=analysis_metadata,
        )

@cache
def get_image_classifier() -> ImageClassifier:
    return ImageClassifier()
