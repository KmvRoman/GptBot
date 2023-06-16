from src.application.common.interfaces import MessengerUserReader, UserReader


class DbGateway(
    UserReader, MessengerUserReader,
):
    pass
