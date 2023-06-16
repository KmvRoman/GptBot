from typing import Protocol

from aiohttp import ClientSession

from src.infrastructure.openai.chat_completion.constants import AiModels
from src.infrastructure.openai.chat_completion.models import AiMessage


class IRequestToOpenAi(Protocol):
    model: AiModels

    def __init__(self, session: ClientSession, chat_completion: str):
        self.session = session
        self.chat_completion = chat_completion

    async def execute(self, content: list[AiMessage]) -> dict:
        raise NotImplementedError
