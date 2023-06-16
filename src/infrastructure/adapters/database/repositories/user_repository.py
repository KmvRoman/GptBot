from datetime import datetime

from sqlalchemy import select, desc

from src.domain.context.entity.constants import Role
from src.domain.context.entity.context import Message, MessageId, ContextId, Context
from src.domain.user.entity.constants import SubLevelEnum
from src.domain.user.entity.user import User, UserId, Subscription, SubscriptionLimit
from src.infrastructure.adapters.database import (
    SystemUser, UserSubscription, RateExpire, Limit, TelegramUser,
    DialogMessage, Reply, TelegramMessage, MessageContext,
    LimitExpire, Channel,
)
from src.infrastructure.adapters.database.exceptions import MessageNotFound
from src.infrastructure.adapters.database.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def create_user(self, user: User) -> User:
        create_user = SystemUser(name=user.name)
        self.session.add(instance=create_user)
        await self.session.flush()
        return User(id=create_user.id, name=create_user.name)

    async def get_user(self, user_id: UserId) -> User:
        user = await self.session.get(entity=SystemUser, ident=user_id)
        return User(id=user.id, name=user.name)

    async def create_user_subscription(self, user_id: UserId, level: SubLevelEnum) -> UserSubscription:
        sub = UserSubscription(user_id=user_id, level=level)
        self.session.add(instance=sub)
        await self.session.flush()
        return sub

    async def create_rate_expire(self, subscription_id: int, expire_at: datetime) -> RateExpire:
        rate_expire = RateExpire(
            subscription_id=subscription_id,
            expire_at=expire_at,
        )
        self.session.add(instance=rate_expire)
        await self.session.flush()
        return rate_expire

    async def create_rate_limit(
            self, subscription_id: int,
            limit: int, expire_at: datetime,
    ) -> Limit:
        limit = Limit(
            subscription_id=subscription_id, limit=limit,
        )
        self.session.add(instance=limit)
        await self.session.flush()
        limit_expire = LimitExpire(limit_id=limit.id, expire_at=expire_at)
        self.session.add(instance=limit_expire)
        await self.session.flush()
        return limit

    async def get_subscription(self, user_id: UserId) -> Subscription:  # TODO: return
        stmt = select(
            UserSubscription.user_id,
            UserSubscription.level,
            RateExpire.expire_at,
            Limit.limit,
            LimitExpire.expire_at,
        ).join(
            SystemUser, SystemUser.id == UserSubscription.user_id
        ).outerjoin(
            RateExpire, RateExpire.subscription_id == UserSubscription.id
        ).outerjoin(
            Limit, Limit.subscription_id == UserSubscription.id
        ).outerjoin(
            LimitExpire, Limit.id == LimitExpire.limit_id
        ).where(SystemUser.id == user_id).order_by(desc(UserSubscription.id))
        sub = (await self.session.execute(stmt)).first()
        return Subscription(
            user_id=sub[0],
            level=sub[1],
            expire_at=sub[2],
            limit=SubscriptionLimit(limit=sub[3], expire_at=sub[4]),
        )

    async def update_limit(self, user_id: UserId, limit: int):
        stmt = select(
            Limit
        ).join(
            UserSubscription, Limit.subscription_id == UserSubscription.id
        ).where(UserSubscription.user_id == user_id).order_by(desc(UserSubscription.id))
        old_limit: Limit = (await self.session.execute(stmt)).scalars().first()
        old_limit.limit = limit

    async def update_limit_expire(self, user_id: UserId, expire: datetime):
        stmt = select(
            LimitExpire
        ).join(
            Limit, Limit.id == LimitExpire.limit_id
        ).join(
            UserSubscription, Limit.subscription_id == UserSubscription.id
        ).where(UserSubscription.user_id == user_id).order_by(desc(LimitExpire.id))
        limit_expire: LimitExpire = (await self.session.execute(stmt)).scalars().first()
        limit_expire.expire_at = expire

    async def get_messenger_user(self, messenger_user_id: int) -> UserId | None:
        stmt = select(
            SystemUser.id,
        ).join(
            TelegramUser, SystemUser.id == TelegramUser.user_id
        ).where(TelegramUser.telegram_user_id == messenger_user_id)
        user_id = (await self.session.execute(stmt)).first()
        if user_id is None:
            return
        return UserId(user_id[0])

    async def create_messenger_user(self, user_id: UserId, messenger_user_id: int) -> None:
        messenger_user = TelegramUser(user_id=user_id, telegram_user_id=messenger_user_id)
        self.session.add(instance=messenger_user)

    async def create_message_dialog(self, role: Role, text: str, context_id: ContextId) -> DialogMessage:
        create_message = DialogMessage(role=role, text=text, context_id=context_id)
        self.session.add(instance=create_message)
        await self.session.flush()
        return create_message

    async def create_reply(self, message_id: MessageId, reply_to: MessageId) -> Reply:
        reply = Reply(message_id=message_id, reply_to=reply_to)
        self.session.add(instance=reply)
        await self.session.flush()
        return reply

    async def get_message(self, message_id: MessageId) -> Message:
        stmt = select(
            DialogMessage.id,
            DialogMessage.role,
            DialogMessage.text,
            DialogMessage.context_id,
            Reply.reply_to,
        ).outerjoin(
            Reply, DialogMessage.id == Reply.message_id
        ).where(DialogMessage.id == message_id)
        get_message = (await self.session.execute(stmt)).first()
        if get_message is None:
            raise MessageNotFound()
        return Message(
            id=get_message[0],
            role=get_message[1],
            text=get_message[2],
            context_id=get_message[3],
            reply_to=get_message[4],
        )

    async def get_messages(
            self, context_id: ContextId,
    ) -> list[Message]:
        stmt = select(
            DialogMessage.id,
            DialogMessage.role,
            DialogMessage.text,
            DialogMessage.context_id,
            Reply.reply_to,
        ).outerjoin(
            Reply, DialogMessage.id == Reply.message_id
        ).where(DialogMessage.context_id == context_id)
        get_messages = (await self.session.execute(stmt)).all()
        return [Message(
            id=message[0],
            role=message[1],
            text=message[2],
            context_id=message[3],
            reply_to=message[4],
        ) for message in get_messages]

    async def get_messenger_message(self, messenger_message_id: int) -> Message:
        stmt = select(
            DialogMessage.id,
            DialogMessage.role,
            DialogMessage.text,
            DialogMessage.context_id,
            Reply.reply_to,
        ).join(
            TelegramMessage, DialogMessage.id == TelegramMessage.message_id
        ).outerjoin(
            Reply, DialogMessage.id == Reply.message_id
        ).where(TelegramMessage.telegram_message_id == messenger_message_id)
        message = (await self.session.execute(stmt)).first()
        if message is None:
            raise MessageNotFound()
        return Message(
            id=message[0],
            role=message[1],
            text=message[2],
            context_id=message[3],
            reply_to=message[4],
        )

    async def create_messenger_message(self, message_id: MessageId, messenger_message_id: int) -> None:
        messenger_message = TelegramMessage(message_id=message_id, telegram_message_id=messenger_message_id)
        self.session.add(messenger_message)
        await self.session.flush()

    async def create_context(self, context: Context) -> Context:
        create_context = MessageContext(user_id=context.user_id, expire=context.expire)
        self.session.add(instance=create_context)
        await self.session.flush()
        return Context(
            id=create_context.id,
            user_id=create_context.user_id,
            expire=create_context.expire,
        )

    async def get_context(self, context_id: ContextId) -> Context:
        context = await self.session.get(entity=MessageContext, ident=context_id)
        return Context(id=context.id, user_id=context.user_id, expire=context.expire)

    async def get_channels_need_to_follow(self):
        stmt = select(
            Channel.chat_id,
        )
        result = (await self.session.execute(stmt)).scalars().all()
        return result
