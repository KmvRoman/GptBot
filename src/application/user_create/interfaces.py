from src.application.common.interfaces import (
    UserCreator, MessengerUserCreator,
    MessengerUserReader, SubscriptionCreator,
)


class DbGateway(
    UserCreator, MessengerUserCreator,
    MessengerUserReader, SubscriptionCreator,
):
    pass
