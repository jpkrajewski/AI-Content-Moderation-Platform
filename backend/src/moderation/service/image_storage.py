import os
from typing import List
from uuid import uuid4

from werkzeug.datastructures import FileStorage


class LocalImageStorage:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    def save_images(self, images: List[FileStorage]) -> List[str]:
        saved_paths = []
        for image in images:
            ext = os.path.splitext(image.filename)[-1]
            filename = f"{uuid4()}{ext}"
            filepath = os.path.abspath(os.path.join(self.upload_dir, filename))
            image.save(filepath)
            saved_paths.append(filepath)

        return saved_paths
