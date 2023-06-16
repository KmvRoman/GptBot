from dataclasses import dataclass
from datetime import datetime

from src.domain.context.entity.context import ContextId


@dataclass
class AccessContextDtoInput:
    context_id: ContextId
    datetime_now: datetime
