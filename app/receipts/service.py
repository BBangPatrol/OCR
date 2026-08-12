from app.receipts.ocr.base import OcrEngine, TextBox


def reconstruct_lines(boxes: list[TextBox], y_tolerance: int = 12) -> str:
    """좌표 기준으로 원래 줄 구조를 복원한다."""
    if not boxes:
        return ""

    lines: list[list[TextBox]] = []
    for box in sorted(boxes, key=lambda b: b.y):
        if lines and abs(box.y - lines[-1][0].y) <= y_tolerance:
            lines[-1].append(box)
        else:
            lines.append([box])

    return "\n".join(
        " ".join(b.text for b in sorted(line, key=lambda b: b.x))
        for line in lines
    )


class ReceiptService:
    def __init__(self, engine: OcrEngine, max_image_bytes: int):
        self.engine = engine
        self.max_image_bytes = max_image_bytes

    async def extract_text(self, image: bytes) -> str:
        if not image:
            raise ValueError("이미지가 비어 있습니다")
        if len(image) > self.max_image_bytes:
            raise ValueError("이미지 크기가 허용치를 초과했습니다")

        boxes = await self.engine.run(image)
        return reconstruct_lines(boxes)