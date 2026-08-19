import logging

import cv2
import numpy as np
from paddleocr import PaddleOCR

from app.receipts.ocr.base import OcrEngine, TextBox


logger = logging.getLogger(__name__)


class PaddleOcrEngine(OcrEngine):

    def __init__(self):
        self.ocr = PaddleOCR(
            lang="korean",

            # 맥북 로컬 환경에서 사용할 수 있도록
            # Server 모델보다 가벼운 Mobile 검출 모델 사용
            text_detection_model_name="PP-OCRv5_mobile_det",

            # 영수증 OCR 정도면 우선 불필요한 전처리는 끄고 시작
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

    # 이미지의 긴 변이 2000픽셀을 넘어갈 경우에만 사이즈 조절
    def resize_if_needed(self, img, max_side: int = 2000):
        h, w = img.shape[:2]

        current_max = max(h, w)

        # 2000 이하라면 그대로 사용
        if current_max <= max_side:
            return img

        scale = max_side / current_max

        new_w = int(w * scale)
        new_h = int(h * scale)

        return cv2.resize(
            img,
            (new_w, new_h),
            interpolation=cv2.INTER_AREA
        )

    async def run(self, image: bytes) -> list[TextBox]:

        # Spring → FastAPI로 넘어온 bytes를 OpenCV 이미지로 변환
        image_array = np.frombuffer(image, dtype=np.uint8)

        img = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR,
        )

        if img is None:
            raise ValueError("이미지를 읽을 수 없습니다")

        logger.info(
            "원본 이미지 크기: %sx%s",
            img.shape[1],
            img.shape[0],
        )

        # 이미지가 2000픽셀 넘어가면 사이즈 조절 수행
        img = self.resize_if_needed(img, max_side=2000)

        logger.info(
            "OCR 입력 이미지 크기: %sx%s",
            img.shape[1],
            img.shape[0],
        )

        logger.info("PaddleOCR 추론 시작")

        results = self.ocr.predict(img)

        logger.info("PaddleOCR 추론 완료")

        boxes: list[TextBox] = []

        for result in results:
            data = result.json["res"]

            texts = data["rec_texts"]
            rects = data["rec_boxes"]

            for text, rect in zip(texts, rects):

                # rect:
                # [x_min, y_min, x_max, y_max]

                x_min = int(rect[0])
                y_min = int(rect[1])

                boxes.append(
                    TextBox(
                        text=text,
                        x=x_min,
                        y=y_min,
                    )
                )

        return boxes