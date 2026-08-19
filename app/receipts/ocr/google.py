import base64
import logging

import httpx

from app.receipts.ocr.base import OcrEngine, TextBox

logger = logging.getLogger(__name__)


class GoogleVisionOcrEngine(OcrEngine):

    VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Google Vision API Key가 설정되지 않았습니다.")

        self.api_key = api_key

    async def run(self, image: bytes) -> list[TextBox]:

        # Google Vision REST API는 이미지 데이터를 Base64 문자열로 전달
        encoded_image = base64.b64encode(image).decode("utf-8")

        request_body = {
            "requests": [
                {
                    "image": {
                        "content": encoded_image
                    },
                    "features": [
                        {
                            "type": "DOCUMENT_TEXT_DETECTION"
                        }
                    ],
                    # 영수증이 한국어 중심이므로 힌트 제공
                    "imageContext": {
                        "languageHints": ["ko"]
                    }
                }
            ]
        }

        logger.info("Google Vision OCR 요청 시작")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.VISION_API_URL,
                headers={
                    "x-goog-api-key": self.api_key,
                    "Content-Type": "application/json",
                },
                json=request_body,
            )

        logger.info(
            "Google Vision OCR 응답 수신 | status=%s",
            response.status_code,
        )

        if response.is_error:
            logger.error(
                "Google Vision OCR 오류 | status=%s | body=%s",
                response.status_code,
                response.text,
            )
            raise RuntimeError("Google Vision OCR 요청에 실패했습니다.")

        data = response.json()

        responses = data.get("responses", [])

        if not responses:
            return []

        result = responses[0]

        # Vision API 자체 오류 확인
        if "error" in result:
            logger.error(
                "Google Vision OCR API 오류: %s",
                result["error"],
            )
            raise RuntimeError("Google Vision OCR 처리 중 오류가 발생했습니다.")

        full_text = result.get("fullTextAnnotation")

        if not full_text:
            return []

        boxes: list[TextBox] = []

        # DOCUMENT_TEXT_DETECTION 결과 구조
        # page → block → paragraph → word
        for page in full_text.get("pages", []):
            for block in page.get("blocks", []):
                for paragraph in block.get("paragraphs", []):
                    for word in paragraph.get("words", []):

                        text = "".join(
                            symbol.get("text", "")
                            for symbol in word.get("symbols", [])
                        )

                        vertices = (
                            word
                            .get("boundingBox", {})
                            .get("vertices", [])
                        )

                        if not text or not vertices:
                            continue

                        x = vertices[0].get("x", 0)
                        y = vertices[0].get("y", 0)

                        boxes.append(
                            TextBox(
                                text=text,
                                x=x,
                                y=y,
                            )
                        )

        logger.info(
            "Google Vision OCR 완료 | 추출 단어 수=%s",
            len(boxes),
        )

        return boxes