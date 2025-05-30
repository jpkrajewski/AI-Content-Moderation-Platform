from typing import List

import numpy as np

from moderation.models.classification import Result

class VideoResultAggregator:
    def __call__(self, results: List[Result]) -> Result:
        flagged_results = [res for res in results if res.automated_flag]
        nsfw_scores = np.array([res.analysis_metadata["nsfw"] for res in results], dtype=np.float32)

        aggregated_metadata = {
            "nsfw": {
                "max": float(nsfw_scores.max()),
                "min": float(nsfw_scores.min()),
                "mean": float(nsfw_scores.mean()),
            },
            "frames": {
                "flagged": [res.analysis_metadata for res in flagged_results],
            }
        }

        first_result = results[0]

        return Result(
            content_type=first_result.content_type,
            model_version=first_result.model_version,
            automated_flag=bool(flagged_results),
            automated_flag_reason="At least one frame is nsfw" if flagged_results else None,
            analysis_metadata=aggregated_metadata,
        )
