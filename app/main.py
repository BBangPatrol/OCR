import logging

from fastapi import FastAPI

from app.core.config import get_settings
from app.receipts.router import router as receipts_router

settings = get_settings()

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(receipts_router, prefix="/api/receipts", tags=["receipts"])


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

# 실행 버튼이 아닌 터미널에서 다음 명령어를 통해서 실행해야 함
# uv run uvicorn app.main:app --reload --port 8000