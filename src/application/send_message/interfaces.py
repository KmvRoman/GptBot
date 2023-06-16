from src.application.common.interfaces import (
    MessengerSendMessage, MessageCreator,
    MessengerMessageCreator,
)


class DbGateway(
    MessageCreator, MessengerMessageCreator,
):
    pass


class MessengerGateway(MessengerSendMessage):
    pass
