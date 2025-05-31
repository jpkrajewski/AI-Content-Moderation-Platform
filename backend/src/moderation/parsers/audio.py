import numpy as np
from pydub import AudioSegment


def samples_from_video_path(video_path: str) -> np.ndarray:
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