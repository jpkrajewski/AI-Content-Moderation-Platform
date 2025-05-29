import asyncio
from pathlib import Path

from moderation.ai.image import get_image_classifier
from moderation.ai.video import VideoClassifier
from moderation.pipelines.video import get_video_pipeline

FOLDER = Path(__file__).parent


def test_image_classifier():
    video_path = str(FOLDER / "file_example_MP4_640_3MG.mp4")
    vc = VideoClassifier(image_classifier=get_image_classifier())
    res = vc.classify_video(video_path)
    print(res)


def test_video_classifier():
    asyncio.run(ccc())



async def ccc():
    resu = await get_video_pipeline().process(
            "/Users/Jakub_Krajewski/PycharmProjects/AI-Content-Moderation-Platform/backend/test/integration/ai/file_example_MP4_640_3MG.mp4")

    print("Video classification result:", resu)
    return resu