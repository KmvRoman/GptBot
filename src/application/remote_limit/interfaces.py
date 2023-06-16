from src.application.common.interfaces import (
    CreateLimit, SubscriptionReader, LimitRefresher,
)


class DbGateway(SubscriptionReader, LimitRefresher, CreateLimit):
    pass
