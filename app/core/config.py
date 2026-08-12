from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "receipt-ocr"
    debug: bool = False

    # OCR 엔진 선택
    ocr_provider: Literal["stub", "clova", "rapid"] = "stub"

    # OCR 제공자 확정 후 채우기
    ocr_api_url: str = ""
    ocr_secret_key: str = ""

    max_image_bytes: int = 10 * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()