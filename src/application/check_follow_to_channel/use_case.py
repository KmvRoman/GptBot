from src.application.check_follow_to_channel.constants import UserChannelStatus
from src.application.check_follow_to_channel.dto import CheckFollowDtoInput
from src.application.check_follow_to_channel.exceptions import UserNotFollowed
from src.application.check_follow_to_channel.interfaces import DbGateway, MessengerGateway
from src.application.common.use_case import UseCase


class CheckToFollow(UseCase[CheckFollowDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, messenger_gateway: MessengerGateway):
        self.db_gateway = db_gateway
        self.messenger_gateway = messenger_gateway

    async def __call__(self, data: CheckFollowDtoInput) -> None:
        base_follows = await self.db_gateway.get_channels_need_to_follow()
        for channel in base_follows:
            member_status = await self.messenger_gateway.get_member(
                chat_id=channel, user_id=data.messenger_user_id,
            )
            if member_status in [
                UserChannelStatus.creator,
                UserChannelStatus.administrator,
                UserChannelStatus.member,
            ]:
                continue
            raise UserNotFollowed()
