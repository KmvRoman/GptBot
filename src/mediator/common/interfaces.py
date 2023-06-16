from abc import abstractmethod
from typing import Protocol

from src.domain.context.entity.context import Message


class Committer(Protocol):
    async def commit(self):
        raise NotImplementedError


class MessengerSendMessage(Protocol):
    @abstractmethod
    async def send_message(self, user_id: int, text: str) -> int:
        raise NotImplementedError


class SendRequestWithoutContext(Protocol):
    @abstractmethod
    async def without_context(self, text: str) -> str:
        raise NotImplementedError


class SendRequestWithContext(Protocol):
    @abstractmethod
    async def with_context(self, messages: list[Message], text: str) -> str:
        raise NotImplementedError
