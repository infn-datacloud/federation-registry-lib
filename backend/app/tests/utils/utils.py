import string
import time
from datetime import date, datetime, timezone
from random import choices, getrandbits, randint, randrange

from pydantic import AnyHttpUrl


def random_lower_string() -> str:
    return "".join(choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_int() -> str:
    return randrange(-100, 100)


def random_non_negative_int() -> int:
    return randrange(100)


def random_positive_int() -> int:
    return randrange(1, 100)


def random_bool() -> bool:
    return getrandbits(1)


def random_datetime() -> datetime:
    d = randint(1, int(time.time()))
    return datetime.fromtimestamp(d, tz=timezone.utc)


def random_date() -> date:
    d = randint(1, int(time.time()))
    return date.fromtimestamp(d)


def random_url() -> AnyHttpUrl:
    return AnyHttpUrl(random_lower_string(), scheme="http")


def random_float() -> float:
    return float(random_int())


def random_positive_float() -> float:
    return float(random_positive_int())


def random_non_negative_float() -> float:
    return float(random_non_negative_int())
