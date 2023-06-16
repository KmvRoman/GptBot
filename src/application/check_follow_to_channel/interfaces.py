from src.application.common.interfaces import GetChatUserStatus, GetChannelsToFollow


class DbGateway(GetChatUserStatus, GetChannelsToFollow):
    pass


class MessengerGateway(GetChatUserStatus):
    pass
