from dataclasses import dataclass
from typing import Protocol


@dataclass
class TextBox:
    text: str
    x: int
    y: int


class OcrEngine(Protocol):
    async def run(self, image: bytes) -> list[TextBox]: ...