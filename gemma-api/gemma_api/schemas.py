from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 200
    temperature: float = 0.7
