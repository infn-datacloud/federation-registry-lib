"""Provider specific fixtures."""
from typing import Optional

from pytest_cases import fixture, parametrize

from app.provider.schemas import ProviderBase


@fixture
@parametrize(attr=[*ProviderBase.__fields__.keys(), "uid", None])
def provider_valid_get_attr(attr: str) -> Optional[str]:
    """Parametrized provider attribute."""
    return attr


@fixture
@parametrize(reverse=[True, False])
@parametrize(attr=[*ProviderBase.__fields__.keys(), "uid"])
def provider_valid_sort_attr(reverse: bool, attr: str) -> Optional[str]:
    """Parametrized provider attribute."""
    if reverse:
        return "-" + attr
    return attr


@fixture
@parametrize(attr=[*ProviderBase.__fields__.keys()])
def provider_patch_attr(attr: str) -> Optional[str]:
    """Parametrized provider attribute."""
    return attr


@fixture
@parametrize(attr=[k for k, v in ProviderBase.__fields__.items() if not v.required])
def provider_valid_patch_default_attr(attr: str) -> Optional[str]:
    """Parametrized provider attribute."""
    return attr


@fixture
@parametrize(attr=[k for k, v in ProviderBase.__fields__.items() if v.required])
def provider_invalid_patch_default_attr(attr: str) -> Optional[str]:
    """Parametrized provider attribute."""
    return attr
