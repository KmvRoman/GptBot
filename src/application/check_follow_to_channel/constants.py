from enum import Enum


class UserChannelStatus(str, Enum):
    creator = "creator"
    administrator = "administrator"
    member = "member"
    restricted = "restricted"
    left = "left"
    kicked = "kicked"
