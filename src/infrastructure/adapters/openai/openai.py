from pydantic import ValidationError

from src.domain.context.entity.constants import Role
from src.domain.context.entity.context import Message
from src.infrastructure.openai.chat_completion.exceptions import SomethingWentWrong
from src.infrastructure.openai.chat_completion.interfaces import IRequestToOpenAi
from src.infrastructure.openai.chat_completion.models import AiMessage, OpenAiResponse


class OpenAiAdapter:
    def __init__(self, openai: IRequestToOpenAi):
        self.openai = openai

    async def without_context(self, text: str) -> str:
        response = await self.openai.execute(content=[AiMessage(role=Role.user.value, content=text)])
        try:
            return OpenAiResponse(**response).choices[0].message.content
        except ValidationError:
            raise SomethingWentWrong()

    async def with_context(self, messages: list[Message]) -> str:
        response = await self.openai.execute(
            content=[AiMessage(role=message.role.value, content=message.text) for message in messages],
        )
        try:
            return OpenAiResponse(**response).choices[0].message.content
        except ValidationError:
            raise SomethingWentWrong()
