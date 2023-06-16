from pydantic import BaseModel

from src.domain.context.entity.constants import Role
from src.infrastructure.openai.chat_completion.constants import AiModels


class AiMessage(BaseModel):
    role: Role
    content: str


class OpenAiRequest(BaseModel):
    model: AiModels
    messages: list[AiMessage]


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Choice(BaseModel):
    message: AiMessage
    finish_reason: str
    index: int


class OpenAiResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: Usage
    choices: list[Choice]
