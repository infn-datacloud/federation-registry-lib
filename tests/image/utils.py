"""Image utilities."""
from random import choice

from app.image.enum import ImageOS


def random_os_type() -> str:
    """Return one of the possible image OS values."""
    return choice([i.value for i in ImageOS])
