from src.application.common.interfaces import ContextReader, MessagesReader


class DbGateway(
    ContextReader, MessagesReader,
):
    pass
