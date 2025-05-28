import os
from abc import ABC, abstractmethod
from functools import cache

import pymupdf
import torch
from docx import Document

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
    try:
        return extractors[ext](document_path)
    except KeyError:
        raise ValueError(f"Unsupported file extension: {ext} for {document_path}")


def extract_text_from_document(document_path: str) -> str:
    return create_extractor(document_path).extract_text()