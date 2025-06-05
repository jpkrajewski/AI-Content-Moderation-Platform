from pathlib import Path
from transformers import (
    pipeline,
    AutoFeatureExtractor,
    AutoModelForImageClassification,
    AutoTokenizer,
    AutoModelForSequenceClassification
)
from moderation.core.settings import settings


# Define base path and subpaths for models
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MODEL_SAVE_BASE_PATH = PROJECT_ROOT / "models"

AUDIO_MODEL_PATH = MODEL_SAVE_BASE_PATH / "audio"
IMAGE_MODEL_PATH = MODEL_SAVE_BASE_PATH / "image"
TEXT_MODEL_PATH = MODEL_SAVE_BASE_PATH / "text"

def download_ai_models():
    """
    Downloads and saves AI models only if they don't already exist locally.
    """

    # --- AUDIO MODEL (Whisper) ---
    if not AUDIO_MODEL_PATH.exists():
        print("⬇️ Downloading audio model...")
        asr_pipeline = pipeline(
            task="automatic-speech-recognition",
            model=settings.AI_AUDIO_MODEL_NAME,
        )
        audio_model = asr_pipeline.model
        audio_tokenizer = asr_pipeline.tokenizer
        audio_feature_extractor = asr_pipeline.feature_extractor

        AUDIO_MODEL_PATH.mkdir(parents=True, exist_ok=True)
        audio_model.save_pretrained(AUDIO_MODEL_PATH)
        audio_tokenizer.save_pretrained(AUDIO_MODEL_PATH)
        audio_feature_extractor.save_pretrained(AUDIO_MODEL_PATH)
    else:
        print("✅ Audio model already exists. Skipping download.")

    # --- IMAGE MODEL (NSFW) ---
    if not IMAGE_MODEL_PATH.exists():
        print("⬇️ Downloading image model...")
        image_extractor = AutoFeatureExtractor.from_pretrained(settings.AI_IMAGE_MODEL_NAME)
        image_model = AutoModelForImageClassification.from_pretrained(settings.AI_IMAGE_MODEL_NAME)

        IMAGE_MODEL_PATH.mkdir(parents=True, exist_ok=True)
        image_model.save_pretrained(IMAGE_MODEL_PATH)
        image_extractor.save_pretrained(IMAGE_MODEL_PATH)
    else:
        print("✅ Image model already exists. Skipping download.")

    # --- TEXT MODEL (Toxicity Detection) ---
    if not TEXT_MODEL_PATH.exists():
        print("⬇️ Downloading text model...")
        text_tokenizer = AutoTokenizer.from_pretrained(settings.AI_TEXT_MODEL_NAME)
        text_model = AutoModelForSequenceClassification.from_pretrained(settings.AI_TEXT_MODEL_NAME)

        TEXT_MODEL_PATH.mkdir(parents=True, exist_ok=True)
        text_model.save_pretrained(TEXT_MODEL_PATH)
        text_tokenizer.save_pretrained(TEXT_MODEL_PATH)
    else:
        print("✅ Text model already exists. Skipping download.")

    print("✅ All model checks completed.")

if __name__ == "__main__":
    download_ai_models()