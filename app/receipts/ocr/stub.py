from app.receipts.ocr.base import OcrEngine, TextBox


class StubOcrEngine(OcrEngine):
    """OCR 제공자 확정 전까지 사용하는 더미 엔진.

    실제 검출 결과처럼 순서가 뒤섞인 박스 목록을 반환한다.
    reconstruct_lines()가 좌표로 원래 줄을 복원해야 정상 텍스트가 나온다.
    """

    async def run(self, image: bytes) -> list[TextBox]:
        return [
            # --- 품목 영역 (검출이 먼저 잡히는 경우가 흔함)
            TextBox("2,200", 280, 321),
            TextBox("소금빵", 40, 320),
            TextBox("4,400", 470, 319),
            TextBox("3", 400, 356),
            TextBox("튀김소보로", 40, 355),
            TextBox("5,100", 470, 357),
            TextBox("1,700", 280, 354),
            TextBox("2", 400, 322),

            # --- 머리말
            TextBox("성심당", 210, 42),
            TextBox("본점", 300, 40),
            TextBox("305-81-12345", 40, 81),
            TextBox("[사업자]", 40, 80),
            TextBox("대전광역시 중구 대종로480번길 15", 40, 111),
            TextBox("TEL", 40, 140),
            TextBox(":", 90, 141),
            TextBox("042-256-4114", 110, 139),

            # --- 품목 이어서
            TextBox("부추빵", 40, 390),
            TextBox("2,600", 470, 391),
            TextBox("2,600", 280, 389),
            TextBox("1", 400, 392),

            # --- 합계 영역
            TextBox("11,000", 470, 430),
            TextBox("과세물품가액", 40, 431),
            TextBox("가", 75, 465),
            TextBox("부", 40, 466),
            TextBox("세", 110, 464),
            TextBox("1,100", 470, 465),
            TextBox("계", 95, 501),
            TextBox("합", 40, 500),
            TextBox("12,100", 470, 499),

            # --- 거래 정보
            TextBox("2026-05-23", 40, 211),
            TextBox("14:32:07", 180, 210),
            TextBox("POS: 03", 40, 240),
            TextBox("영수증번호: 0142", 200, 241),
            TextBox("상품명", 40, 281),
            TextBox("단가", 280, 280),
            TextBox("수량", 400, 282),
            TextBox("금액", 470, 280),

            # --- 결제 정보
            TextBox("승인번호", 40, 615),
            TextBox("30215498", 200, 616),
            TextBox("신용카드", 40, 545),
            TextBox("12,100", 470, 546),
            TextBox("5327-**-****-1234", 200, 580),
            TextBox("카드번호", 40, 581),
            TextBox("일시불", 200, 650),
            TextBox("할부", 40, 651),
            TextBox("감사합니다", 200, 700),
        ]