from abc import ABC, abstractmethod
from functools import cache

from moderation.ai.models import ClassifyResult
from moderation.core.settings import settings
from PIL import Image

try:
    import torch
    from transformers import AutoFeatureExtractor, AutoModelForImageClassification
except ImportError:
    if not settings.AI_USE_MOCK:
        raise ImportError(
            "The required libraries for image moderation are not installed. "
            "Please install the necessary libraries or set AI_USE_MOCK to True."
        )


class ImageClassifier(ABC):
    """
    Abstract base class for image classifiers.
    """

    @abstractmethod
    def classify(self, image_path: str) -> ClassifyResult: ...


class ImageModeration(ImageClassifier):
    def __init__(self) -> None:

        self.extractor: AutoFeatureExtractor = AutoFeatureExtractor.from_pretrained(settings.AI_IMAGE_MODERATION_MODEL)
        self.model: AutoModelForImageClassification = AutoModelForImageClassification.from_pretrained(
            settings.AI_IMAGE_MODERATION_MODEL
        )

    def classify(self, image_path: str) -> ClassifyResult:
        """
        Moderates an image using a pre-trained model.
        Args:
            image_path (str): Path to the image file.
        Returns:
            dict: A dictionary with class labels and their corresponding probabilities.

        Example:
            >>> image_moderation = ImageModeration()
            >>> results = image_moderation.moderate_image("path/to/image.jpg")
            >>> print(results)
            {'normal': 0.95, 'nsfw': 0.05}
        """
        image = Image.open(image_path)
        inputs = self.extractor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

        # Map class indices to labels
        labels = self.model.config.id2label
        analysis_metadata = {labels[idx]: score.item() for idx, score in enumerate(probs[0])}
        flagged = analysis_metadata["nsfw"] > settings.AI_IMAGE_MODERATION_THRESHOLD
        flagged_reason = "NSFW content detected" if flagged else ""
        return ClassifyResult(
            content_type="image",
            automated_flag=flagged,
            automated_flag_reason=flagged_reason,
            model_version=settings.AI_IMAGE_MODERATION_MODEL,
            analysis_metadata=analysis_metadata,
        )


class ImageModerationFake(ImageClassifier):
    def classify(self, image_path: str) -> ClassifyResult:
        return ClassifyResult(
            content_type="image",
            automated_flag=False,
            automated_flag_reason="",
            model_version="fake_model",
            analysis_metadata={},
        )


@cache
def get_image_moderation() -> ImageClassifier:
    """Get the image moderation instance."""
    if settings.AI_USE_MOCK:
        return ImageModerationFake()
    return ImageModeration()
