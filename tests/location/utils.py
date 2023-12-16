"""Location utilities."""
from random import choice, randrange

from pycountry import countries


def random_country() -> str:
    """Return random country."""
    return choice([i.name for i in countries])


def random_latitude() -> float:
    """Return random acceptable value for latitude."""
    return float(randrange(-180, 180))


def random_longitude() -> float:
    """Return random acceptable value for longitude."""
    return float(randrange(-90, 90))
