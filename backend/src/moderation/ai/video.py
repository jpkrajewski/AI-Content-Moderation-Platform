import cv2
from pathlib import Path


class VideoClassifier:
    def __init__(self, image_classifier):
        self.image_classifier = image_classifier  # Your image model (e.g., torchvision, transformers pipeline)

    def classify_video(self, video_path: str, frame_interval: int = 10):
        cap = cv2.VideoCapture(str(video_path))
        frame_id = 0
        predictions = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_id % frame_interval == 0:
                # Convert BGR (OpenCV) to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Pass the frame to your image classifier
                result = self.image_classifier.classify_(frame_rgb)
                predictions.append(result)

            frame_id += 1

        cap.release()
        return predictions