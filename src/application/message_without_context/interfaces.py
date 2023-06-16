from src.application.common.interfaces import MessageCreator, MessengerMessageCreator, ContextCreator, \
    SendRequestWithoutContext


class DbGateway(
    MessageCreator, MessengerMessageCreator, ContextCreator,
):
    pass


class RequestToApi(SendRequestWithoutContext):
    pass
