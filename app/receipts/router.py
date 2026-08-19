import logging
from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import Settings, get_settings
from app.receipts.ocr.base import OcrEngine
from app.receipts.schema import OcrTextResponse
from app.receipts.service import ReceiptService


logger = logging.getLogger(__name__)

router = APIRouter()


@lru_cache
def create_engine(
        provider: str,
        api_key: str,
) -> OcrEngine:
    """
    OCR 엔진을 한 번만 생성해서 재사용한다.

    provider 값에 따라 Google Vision / Paddle / Stub 중 하나를 생성하고,
    같은 설정으로 다시 호출되면 lru_cache에 저장된 기존 엔진을 반환한다.
    """

    # Google Vision OCR을 사용할 경우
    if provider == "google":
        from app.receipts.ocr.google import GoogleVisionOcrEngine

        return GoogleVisionOcrEngine(
            api_key=api_key
        )

    # Paddle OCR을 사용할 경우
    if provider == "paddle":
        from app.receipts.ocr.paddle import PaddleOcrEngine

        return PaddleOcrEngine()

    # 테스트용 Stub OCR
    from app.receipts.ocr.stub import StubOcrEngine

    return StubOcrEngine()


def get_engine(  # 조건에 따라 google이랑 paddle이랑 stub 사용 가능
        settings: Settings = Depends(get_settings),
) -> OcrEngine:

    return create_engine(
        settings.ocr_provider,
        settings.google_vision_api_key,
    )


def get_service(
        engine: OcrEngine = Depends(get_engine),
        settings: Settings = Depends(get_settings),
) -> ReceiptService:
    return ReceiptService(
        engine=engine,
        max_image_bytes=settings.max_image_bytes
    )


@router.post("/extract", response_model=OcrTextResponse)
async def extract_text(
        file: UploadFile = File(...),
        service: ReceiptService = Depends(get_service),
) -> OcrTextResponse:
    image = await file.read()

    logger.info(
        "이미지 수신 | name=%s | ext=%s | type=%s | size=%.1fKB",
        file.filename or "(없음)",
        Path(file.filename).suffix.lower() if file.filename else "(없음)",
        file.content_type or "(없음)",
        len(image) / 1024,
        )

    try:
        text = await service.extract_text(image)
    except ValueError as e:
        raise HTTPException(400, str(e)) from e

    return OcrTextResponse(text=text)