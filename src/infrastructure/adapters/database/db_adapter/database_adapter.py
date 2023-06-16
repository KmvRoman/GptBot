from src.domain.context.entity.context import Message, MessageId, ContextId, Context
from src.domain.user.entity.user import User, Subscription, UserId
from src.infrastructure.adapters.database.repositories.user_repository import UserRepository


class DatabaseAdapter:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def commit(self):
        await self.repo.commit()

    async def rollback(self):
        await self.repo.rollback()

    async def create_user(self, user: User) -> User:
        return await self.repo.create_user(user=user)

    async def create_subscription(self, subscription: Subscription) -> Subscription:
        sub = await self.repo.create_user_subscription(
            user_id=subscription.user_id, level=subscription.level,
        )
        if subscription.expire_at is not None:
            await self.repo.create_rate_expire(
                subscription_id=sub.id, expire_at=subscription.expire_at,
            )
        if subscription.limit is not None:
            await self.repo.create_rate_limit(
                subscription_id=sub.id, limit=subscription.limit.limit,
                expire_at=subscription.limit.expire_at,
            )
        return Subscription(
            user_id=sub.user_id, level=sub.level,
            expire_at=subscription.expire_at, limit=subscription.limit,
        )

    async def get_subscription(self, user_id: UserId) -> Subscription:
        return await self.repo.get_subscription(user_id=user_id)

    async def refresh_limit(self, subscription: Subscription):
        if subscription.limit is not None:
            await self.repo.update_limit(
                user_id=subscription.user_id, limit=subscription.limit.limit,
            )
            await self.repo.update_limit_expire(user_id=subscription.user_id, expire=subscription.limit.expire_at)

    async def get_messenger_user(self, messenger_user_id: int) -> UserId | None:
        return await self.repo.get_messenger_user(messenger_user_id=messenger_user_id)

    async def create_messenger_user(self, user_id: UserId, messenger_user_id: int):
        await self.repo.create_messenger_user(user_id=user_id, messenger_user_id=messenger_user_id)

    async def create_message(self, message: Message) -> Message:
        message_create = await self.repo.create_message_dialog(
            role=message.role, text=message.text, context_id=message.context_id,
        )
        if message.reply_to:
            reply = await self.repo.create_reply(message_id=message_create.id, reply_to=message.reply_to)
            return Message(
                id=message_create.id,
                role=message_create.role,
                text=message_create.text,
                context_id=message_create.context_id,
                reply_to=reply.reply_to,
            )
        return Message(
            id=message_create.id,
            role=message_create.role,
            text=message_create.text,
            context_id=message_create.context_id,
            reply_to=None,
        )

    async def get_message(self, message_id: MessageId) -> Message:
        return await self.repo.get_message(message_id=message_id)

    async def get_messages(self, context_id: ContextId) -> list[Message]:
        return await self.repo.get_messages(context_id=context_id)

    async def get_messenger_message(self, messenger_message_id: int) -> Message:
        return await self.repo.get_messenger_message(
            messenger_message_id=messenger_message_id,
        )

    async def create_messenger_message(self, message_id: MessageId, messenger_message_id: int) -> None:
        return await self.repo.create_messenger_message(
            message_id=message_id, messenger_message_id=messenger_message_id,
        )

    async def create_context(self, context: Context) -> Context:
        return await self.repo.create_context(context=context)

    async def get_context(self, context_id: ContextId) -> Context:
        return await self.repo.get_context(context_id=context_id)

    async def get_channels_need_to_follow(self):
        return await self.repo.get_channels_need_to_follow()
