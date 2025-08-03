from pydantic import BaseModel


# Request model
class ChatRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 200
    temperature: float = 0.7
