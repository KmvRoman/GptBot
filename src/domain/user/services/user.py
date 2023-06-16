from src.domain.user.entity.user import User


class UserService:
    def create_user(self, name: str) -> User:
        return User(
            id=None,
            name=name[:25],
        )
