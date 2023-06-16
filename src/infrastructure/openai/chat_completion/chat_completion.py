from aiohttp import ClientSession

from src.infrastructure.openai.chat_completion.constants import AiModels
from src.infrastructure.openai.chat_completion.models import AiMessage, OpenAiRequest


class RequestToOpenAi:
    model = AiModels.chat_gpt_35

    def __init__(self, session: ClientSession, api_key: str, chat_completion: str):
        self.session = session
        self.api_key = api_key
        self.chat_completion = chat_completion

    async def execute(self, content: list[AiMessage]) -> dict:
        response = await self.session.post(
            url=self.chat_completion,
            data=OpenAiRequest(model=self.model.value, messages=content).json(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
        )
        return await response.json()
