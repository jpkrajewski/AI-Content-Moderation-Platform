import os
from dataclasses import dataclass
from pathlib import Path
from typing import List
from uuid import uuid4

from moderation.core.settings import settings
from werkzeug.datastructures import FileStorage


@dataclass
class StoredFile:
    filename: str
    filepath: str


@dataclass
class StoredFiles:
    files: List[StoredFile]

    @property
    def filepaths(self) -> List[str]:
        return [image.filepath for image in self.files]

    @property
    def filenames(self) -> List[str]:
        return [image.filename for image in self.files]


class Storage:
    def __init__(self, upload_dir: Path = settings.APP_UPLOAD_DIR):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    def save(self, images: List[FileStorage]) -> StoredFiles:
        saved_paths: List[StoredFile] = []
        for image in images:
            ext = os.path.splitext(image.filename)[-1]
            filename = f"{uuid4()}{ext}"
            filepath = self.upload_dir / filename
            image.save(filepath)
            saved_paths.append(StoredFile(filename=filename, filepath=str(filepath)))
        return StoredFiles(files=saved_paths)
