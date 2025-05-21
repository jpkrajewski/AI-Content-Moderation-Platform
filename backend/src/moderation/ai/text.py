import os
from abc import ABC, abstractmethod
from functools import cache

import pymupdf
import torch
from docx import Document
from moderation.ai.models import ClassifyResult
from moderation.core.settings import settings
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class TextClassifier(ABC):
    @abstractmethod
    def classify(self, text: str) -> ClassifyResult: ...


class DocumentTextExtractor(ABC):
    @abstractmethod
    def __init__(self, document_path: str) -> None: ...

    @abstractmethod
    def extract_text(self) -> str: ...


class PDFTextExtractor(DocumentTextExtractor):
    def __init__(self, document_path: str) -> None:
        self.document_path = document_path

    def extract_text(self) -> str:
        doc = pymupdf.open(self.document_path)
        text = []
        for page in doc:
            text.append(page.get_text())
        return " ".join(text)


class WordTextExtractor(DocumentTextExtractor):
    def __init__(self, document_path: str) -> None:
        self.document_path = document_path

    def extract_text(self) -> str:
        doc = Document(self.document_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])


def create_extractor(document_path: str) -> DocumentTextExtractor:
    ext = os.path.splitext(document_path)[-1].lower().strip(".")
    extractors: dict[str, type[DocumentTextExtractor]] = {
        "pdf": PDFTextExtractor,
        "doc": WordTextExtractor,
        "docx": WordTextExtractor,
        "odt": WordTextExtractor,
        "rtf": WordTextExtractor,
    }

    if ext in extractors:
        return extractors[ext](document_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext} for {document_path}")


def extract_text_from_document(document_path: str) -> str:
    return create_extractor(document_path).extract_text()


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

    def classify_from_document(self, document_path: str) -> ClassifyResult:
        text = extract_text_from_document(document_path)
        result = self.classify(text)
        result.content_type = "document"
        return result


@cache
def get_text_classifier() -> TextClassifier:
    return TextModeration()
