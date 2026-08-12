from pydantic import BaseModel

class OcrTextResponse(BaseModel):
    text: str