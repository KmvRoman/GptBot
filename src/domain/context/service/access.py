from datetime import datetime

from src.domain.context.entity.constants import FullCapacityContext
from src.domain.context.entity.context import Context, Message
from src.domain.context.exceptions.access import ContextExpired, ContextIsFull


class ContextAccessService:
    def can_continue_context(self, context: Context, datetime_now: datetime):
        if context.expire <= datetime_now:
            raise ContextExpired()

    def is_context_full(self, contexts_messages: list[Message]):
        if len(contexts_messages) == FullCapacityContext.capacity.value:
            raise ContextIsFull()
