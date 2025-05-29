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


class VideoToAudio:
    def __call__(self, video_path: str) -> np.ndarray:
        audio_segment = AudioSegment.from_file(video_path)
        samples = np.array(audio_segment.get_array_of_samples())
        # If stereo, reshape to (num_samples, num_channels)
        if audio_segment.channels == 2:
            samples = samples.reshape((-1, 2))
        # Normalize to float32 in range [-1, 1]
        sample_width = audio_segment.sample_width  # bytes per sample
        max_val = float(2 ** (8 * sample_width - 1))
        samples = samples.astype(np.float32) / max_val
        if len(samples.shape) > 1 and samples.shape[1] > 1:
            samples = samples.mean(axis=1)
        return samples


class VideoToFrames:
    def __init__(self, frame_interval: int = 1):
        self.frame_interval = frame_interval

    def __call__(self, video_path: str) -> np.ndarray:
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frames = []
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if count % int(fps * self.frame_interval) == 0:
                frames.append(frame)  # frame is a NumPy array
            count += 1
        cap.release()
        return frames