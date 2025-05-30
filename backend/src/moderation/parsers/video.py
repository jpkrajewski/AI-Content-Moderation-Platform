import cv2
import numpy as np
from moderation.core.settings import settings


def frames_with_timestamp_from_video_path(video_path: str) -> np.ndarray:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        raise ValueError(f"Invalid FPS from video: {fps}")

    frames_with_timestamps = []
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % int(fps * settings.PARSERS_VIDEO_FRAME_INTERVAL) == 0:
            timestamp = count / fps
            frames_with_timestamps.append((frame, timestamp))
        count += 1

    cap.release()
    return frames_with_timestamps
