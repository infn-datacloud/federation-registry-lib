from enum import Enum


class Status(Enum):
    ACTIVE: str = "active"
    MAINTENANCE: str = "maintenance"
    REMOVED: str = "removed"