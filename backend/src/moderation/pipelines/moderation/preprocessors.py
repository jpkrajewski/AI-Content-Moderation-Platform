import cv2
import numpy as np
from PIL.Image import Image
from pydub import AudioSegment


class ImageFromPath:
    def __call__(self, path: str) -> Image:
        return Image.open(path).convert("RGB")


class ImageFromNumpyArray:
    def __call__(self, array: np.ndarray) -> Image:
        return Image.fromarray(array).convert("RGB")