from enum import Enum


class FullCapacityContext(int, Enum):
    capacity = 30


class Role(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"
