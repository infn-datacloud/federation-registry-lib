"""Tests utilities."""
import string
import time
from datetime import date, datetime, timezone
from random import choices, getrandbits, randint, randrange
from typing import Tuple, Type

from pydantic import AnyHttpUrl

from app.models import BaseNodeRead


def random_lower_string() -> str:
    """Return a generic random string."""
    return "".join(choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    """Return a generic email."""
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_int() -> str:
    """Return a generic integer."""
    return randrange(-100, 100)


def random_non_negative_int() -> int:
    """Return a generic non negative integer.

    0 included.
    """
    return randrange(100)


def random_positive_int() -> int:
    """Return a generic positive integer.

    0 excluded.
    """
    return randrange(1, 100)


def random_bool() -> bool:
    """Return a random bool."""
    return getrandbits(1)


def random_datetime() -> datetime:
    """Return a random date and time."""
    d = randint(1, int(time.time()))
    return datetime.fromtimestamp(d, tz=timezone.utc)


def random_date() -> date:
    """Return a random date."""
    d = randint(1, int(time.time()))
    return date.fromtimestamp(d)


def random_url() -> AnyHttpUrl:
    """Return a random URL."""
    return "http://" + random_lower_string() + ".com"


def random_float() -> float:
    """Return a generic float."""
    return float(random_int())


def random_positive_float() -> float:
    """Return a generic positive float.

    0 excluded.
    """
    return float(random_positive_int())


def random_non_negative_float() -> float:
    """Return a generic positive float.

    0 included.
    """
    return float(random_non_negative_int())


def detect_public_extended_details(read_class: Type[BaseNodeRead]) -> Tuple[bool, bool]:
    """From class name detect if it public or not, extended or not."""
    cls_name = read_class.__name__
    is_public = False
    is_extended = False
    if "Public" in cls_name:
        is_public = True
    if "Extended" in cls_name:
        is_extended = True
    return is_public, is_extended
