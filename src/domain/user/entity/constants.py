from enum import Enum


class SubLevelEnum(str, Enum):
    free = "free"
    low = "low"
    medium = "medium"
    unlimited = "unlimited"


class MessageCount(int, Enum):
    free = 10
    low = 100
    medium = 1000


class SubLevelPrice(float, Enum):
    low = 4.99
    medium = 9.99
    unlimited = 18.99
