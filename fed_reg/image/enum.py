"""Image specific enumerations."""
from enum import Enum


class ImageOS(Enum):
    """Possible operating systems types."""

    Linux: str = "Linux"
    Windows: str = "Windows"
    MacOS: str = "MacOS"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None
