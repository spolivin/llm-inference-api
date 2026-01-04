from pydantic import BaseModel


class GenerateRequest(BaseModel):
    prompt: str
    steps: int = 40
    guidance: float = 7.5
    height: int = 512
    width: int = 512
