from pathlib import Path
import os


class Settings:
    def __init__(self):
        self.hf_token = os.getenv("HF_TOKEN", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.weather_api_key = os.getenv("WEATHER_API_KEY", "")
        self.maps_api_key = os.getenv("MAPS_API_KEY", "")
        self.model_name = os.getenv("MODEL_NAME", "distilbert-base-uncased")
        self.data_dir = Path(__file__).resolve().parent.parent.parent.parent / "data"


settings = Settings()