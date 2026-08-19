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

    # OCR 엔진 선택 지금은 스텁이랑 패들만 있고, 실제 쓸 때는 패들로 변경
    ocr_provider: Literal["stub", "paddle", "google"] = "google"

    # OCR 제공자 확정 후 채우기
    google_vision_api_key: str = ""

    max_image_bytes: int = 10 * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()