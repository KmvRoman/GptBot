from abc import abstractmethod
from typing import Protocol

from src.application.access_context.use_case import AccessContext
from src.application.available_user.use_case import AvailableUser
from src.application.check_follow_to_channel.use_case import CheckToFollow
from src.application.message_with_context.use_case import CreateMessageWithContext
from src.application.message_without_context.use_case import CreateMessageWithoutContext
from src.application.messenger_message_reader.use_case import MessengerMessageToMessage
from src.application.remote_limit.use_case import CreateLimit
from src.application.send_message.use_case import SendMessage
from src.application.set_rate.use_case import SetRate
from src.application.user_create.use_case import CreateUser


class InteractorFactory(Protocol):
    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def check_available(self) -> AvailableUser: ...

    @abstractmethod
    async def create_user(self) -> CreateUser: ...

    @abstractmethod
    async def check_follow_to_channel(self) -> CheckToFollow: ...

    @abstractmethod
    async def messenger_message_reader(self) -> MessengerMessageToMessage: ...

    @abstractmethod
    async def remote_limit(self) -> CreateLimit: ...

    @abstractmethod
    async def send_message(self) -> SendMessage: ...

    @abstractmethod
    async def message_without_context(self) -> CreateMessageWithoutContext: ...

    @abstractmethod
    async def message_with_context(self) -> CreateMessageWithContext: ...

    @abstractmethod
    async def access_context(self) -> AccessContext: ...

    @abstractmethod
    async def set_rate(self) -> SetRate: ...
