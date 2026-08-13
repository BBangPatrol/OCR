import logging
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import Settings, get_settings
from app.receipts.ocr.base import OcrEngine
from app.receipts.schema import OcrTextResponse
from app.receipts.service import ReceiptService

logger = logging.getLogger(__name__)

router = APIRouter()


def get_engine(settings: Settings = Depends(get_settings)) -> OcrEngine:
    from app.receipts.ocr.stub import StubOcrEngine
    return StubOcrEngine()


def get_service(
        engine: OcrEngine = Depends(get_engine),
        settings: Settings = Depends(get_settings),
) -> ReceiptService:
    return ReceiptService(engine=engine, max_image_bytes=settings.max_image_bytes)


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