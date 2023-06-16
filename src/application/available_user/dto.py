from dataclasses import dataclass

from src.domain.user.entity.user import UserId


@dataclass
class CheckUserDtoInput:
    messenger_user_id: int
    name: str


@dataclass
class UserDtoOutput:
    user_id: UserId
