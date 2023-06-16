from src.application.common.interfaces import (
    SendRequestWithContext, MessageCreator, MessagesReader,
)


class DbGateway(
    MessageCreator, MessagesReader,
):
    pass


class RequestToApi(SendRequestWithContext):
    pass
