import os
from dataclasses import dataclass
from pathlib import Path
from typing import List
from uuid import uuid4

from moderation.core.settings import settings
from werkzeug.datastructures import FileStorage


@dataclass
class StoredImage:
    filename: str
    filepath: str


@dataclass
class StoredImages:
    images: List[StoredImage]

    @property
    def paths(self) -> List[str]:
        return [image.filepath for image in self.images]

    @property
    def filenames(self) -> List[str]:
        return [image.filename for image in self.images]


class LocalImageStorage:
    def __init__(self, upload_dir: Path = settings.APP_UPLOAD_DIR):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    def save_images(self, images: List[FileStorage]) -> StoredImages:
        saved_paths: List[StoredImage] = []
        for image in images:
            ext = os.path.splitext(image.filename)[-1]
            filename = f"{uuid4()}{ext}"
            filepath = self.upload_dir / filename
            image.save(filepath)
            saved_paths.append(StoredImage(filename=filename, filepath=str(filepath)))
        return StoredImages(images=saved_paths)
