from abc import abstractmethod
from typing import Protocol

from src.application.check_follow_to_channel.constants import UserChannelStatus
from src.domain.context.entity.context import Message, MessageId, Context, ContextId
from src.domain.user.entity.user import User, UserId, Subscription


class UserCreator(Protocol):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        raise NotImplementedError


class UserReader(Protocol):
    @abstractmethod
    async def get_user(self, user_id: UserId) -> User:
        raise NotImplementedError


class SubscriptionCreator(Protocol):
    @abstractmethod
    async def create_subscription(self, subscription: Subscription) -> None:
        raise NotImplementedError


class SubscriptionReader(Protocol):
    @abstractmethod
    async def get_subscription(self, user_id: UserId) -> Subscription:
        raise NotImplementedError


class LimitRefresher(Protocol):
    @abstractmethod
    async def refresh_limit(self, subscription: Subscription):
        raise NotImplementedError


class MessengerUserReader(Protocol):
    @abstractmethod
    async def get_messenger_user(self, messenger_user_id: int) -> UserId:
        raise NotImplementedError


class MessengerUserCreator(Protocol):
    @abstractmethod
    async def create_messenger_user(self, user_id: UserId, messenger_user_id: int) -> None:
        raise NotImplementedError


class MessageCreator(Protocol):
    @abstractmethod
    async def create_message(self, message: Message) -> Message:
        raise NotImplementedError


class MessageReader(Protocol):
    @abstractmethod
    async def get_message(self, message_id: MessageId) -> Message:
        raise NotImplementedError


class MessagesReader(Protocol):
    @abstractmethod
    async def get_messages(self, context_id: ContextId) -> list[Message]:
        raise NotImplementedError


class MessengerMessageCreator(Protocol):
    @abstractmethod
    async def create_messenger_message(self, message_id: MessageId, messenger_message_id: int) -> None:
        raise NotImplementedError


class MessengerMessageReader(Protocol):
    @abstractmethod
    async def get_messenger_message(self, messenger_message_id: int) -> Message:
        raise NotImplementedError


class ContextCreator(Protocol):
    @abstractmethod
    async def create_context(self, context: Context) -> Context:
        raise NotImplementedError


class ContextReader(Protocol):
    @abstractmethod
    async def get_context(self, context_id: ContextId) -> Context:
        raise NotImplementedError


class CreateLimit(Protocol):
    @abstractmethod
    async def create_limit(self, user_id: UserId, limit: int) -> None:
        raise NotImplementedError


class GetChannelsToFollow(Protocol):
    @abstractmethod
    async def get_channels_need_to_follow(self) -> list[int]:
        raise NotImplementedError


class SendRequestWithoutContext(Protocol):
    @abstractmethod
    async def without_context(self, text: str) -> str:
        raise NotImplementedError


class SendRequestWithContext(Protocol):
    @abstractmethod
    async def with_context(self, messages: list[Message]) -> str:
        raise NotImplementedError


class MessengerSendMessage(Protocol):
    @abstractmethod
    async def send_message(self, chat_id: int, text: str, reply_to_message: int) -> int:
        raise NotImplementedError


class GetChatUserStatus:
    @abstractmethod
    async def get_member(self, chat_id: int, user_id: int) -> UserChannelStatus:
        raise NotImplementedError
