from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.project.schemas import ProjectCreate
from fed_reg.provider.models import Provider
from fed_reg.provider.schemas import (
    ProviderBase,
    ProviderBasePublic,
    ProviderRead,
    ProviderReadPublic,
)
from fed_reg.provider.schemas_extended import (
    IdentityProviderCreateExtended,
    ProviderCreateExtended,
    RegionCreateExtended,
)
from tests.create_dict import provider_schema_dict
from tests.utils import random_lower_string


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_base_public(key: str, value: Any) -> None:
    d = provider_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProviderBasePublic(**d)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_base(key: str, value: Any) -> None:
    d = provider_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProviderBase(**d)


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_read_public(provider_model: Provider, key: str, value: str) -> None:
    provider_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ProviderReadPublic.from_orm(provider_model)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_read(provider_model: Provider, key: str, value: str) -> None:
    provider_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ProviderRead.from_orm(provider_model)


@parametrize_with_cases("attr, values, msg", has_tag="create_extended")
def test_invalid_create_extended(
    attr: str,
    values: list[IdentityProviderCreateExtended]
    | list[ProjectCreate]
    | list[RegionCreateExtended],
    msg: str,
) -> None:
    d = provider_schema_dict()
    d[attr] = values
    if attr == "identity_providers":
        projects = set()
        for idp in values:
            for user_group in idp.user_groups:
                projects.add(user_group.sla.project)
        d["projects"] = [
            ProjectCreate(name=random_lower_string(), uuid=p) for p in projects
        ]
    with pytest.raises(ValueError, match=msg):
        ProviderCreateExtended(**d)


@parametrize_with_cases("identity_providers, msg", has_tag="idps")
def test_dup_proj_in_idps_in_create_extended(
    identity_providers: list[IdentityProviderCreateExtended]
    | list[ProjectCreate]
    | list[RegionCreateExtended],
    msg: str,
) -> None:
    d = provider_schema_dict()
    d["identity_providers"] = identity_providers
    projects = set()
    for idp in identity_providers:
        for user_group in idp.user_groups:
            projects.add(user_group.sla.project)
    d["projects"] = [
        ProjectCreate(name=random_lower_string(), uuid=p) for p in projects
    ]
    with pytest.raises(ValueError, match=msg):
        ProviderCreateExtended(**d)


@parametrize_with_cases("attr, values, msg", has_tag="missing")
def test_miss_proj_in_idps_in_create_extended(
    attr: str,
    values: list[IdentityProviderCreateExtended] | list[RegionCreateExtended],
    msg: str,
) -> None:
    d = provider_schema_dict()
    d[attr] = values
    with pytest.raises(ValueError, match=msg):
        ProviderCreateExtended(**d)
