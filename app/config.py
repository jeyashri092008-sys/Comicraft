import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GEMINI_STORY_MODEL: str = os.getenv("GEMINI_STORY_MODEL", "gemini-2.5-flash")
    IMAGE_PROVIDER: str = os.getenv("IMAGE_PROVIDER", "huggingface")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    HUGGINGFACE_IMAGE_MODEL: str = os.getenv("HUGGINGFACE_IMAGE_MODEL", "stabilityai/stable-diffusion-xl-base-1.0")

    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR: str = os.path.join(BASE_DIR, "static")
    TEMPLATES_DIR: str = os.path.join(BASE_DIR, "templates")
    PANELS_DIR: str = os.path.join(STATIC_DIR, "panels")
    EXPORTS_DIR: str = os.path.join(STATIC_DIR, "exports")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
