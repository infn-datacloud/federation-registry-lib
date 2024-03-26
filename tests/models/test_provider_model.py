from typing import Any, List, Literal, Tuple

import pytest
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.auth_method.models import AuthMethod
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.project.models import Project
from fed_reg.provider.models import Provider
from fed_reg.region.models import Region
from tests.create_dict import (
    auth_method_dict,
    identity_provider_model_dict,
    project_model_dict,
    provider_model_dict,
    region_model_dict,
)
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "type"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description", "status"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()

    @parametrize(key=["is_public"])
    def case_bool(self, key: str) -> Tuple[str, Literal[True]]:
        return key, True

    @parametrize(key=["empty", "full"])
    def case_list_str(self, key: str) -> Tuple[str, List[str]]:
        if key == "empty":
            return key, []
        return key, [random_lower_string()]


def test_default_attr() -> None:
    d = provider_model_dict()
    item = Provider(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.type == d.get("type")
    assert item.is_public is False
    assert item.status is None
    assert item.support_emails == []
    assert isinstance(item.projects, RelationshipManager)
    assert isinstance(item.regions, RelationshipManager)
    assert isinstance(item.identity_providers, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = provider_model_dict()
    d[missing_attr] = None
    item = Provider(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(key: str, value: Any) -> None:
    d = provider_model_dict()
    d[key] = value

    item = Provider(**d)
    saved = item.save()

    assert saved.element_id_property
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_optional_rel(provider_model: Provider) -> None:
    assert len(provider_model.identity_providers.all()) == 0
    assert provider_model.identity_providers.single() is None
    assert len(provider_model.projects.all()) == 0
    assert provider_model.projects.single() is None
    assert len(provider_model.regions.all()) == 0
    assert provider_model.regions.single() is None


def test_linked_project(provider_model: Provider, project_model: Project) -> None:
    assert provider_model.projects.name
    assert provider_model.projects.source
    assert isinstance(provider_model.projects.source, Provider)
    assert provider_model.projects.source.uid == provider_model.uid
    assert provider_model.projects.definition
    assert provider_model.projects.definition["node_class"] == Project

    r = provider_model.projects.connect(project_model)
    assert r is True

    assert len(provider_model.projects.all()) == 1
    project = provider_model.projects.single()
    assert isinstance(project, Project)
    assert project.uid == project_model.uid


def test_multiple_linked_projects(provider_model: Provider) -> None:
    item = Project(**project_model_dict()).save()
    provider_model.projects.connect(item)
    item = Project(**project_model_dict()).save()
    provider_model.projects.connect(item)
    assert len(provider_model.projects.all()) == 2


def test_linked_region(provider_model: Provider, region_model: Region) -> None:
    assert provider_model.regions.name
    assert provider_model.regions.source
    assert isinstance(provider_model.regions.source, Provider)
    assert provider_model.regions.source.uid == provider_model.uid
    assert provider_model.regions.definition
    assert provider_model.regions.definition["node_class"] == Region

    r = provider_model.regions.connect(region_model)
    assert r is True

    assert len(provider_model.regions.all()) == 1
    region = provider_model.regions.single()
    assert isinstance(region, Region)
    assert region.uid == region_model.uid


def test_multiple_linked_regions(provider_model: Provider) -> None:
    item = Region(**region_model_dict()).save()
    provider_model.regions.connect(item)
    item = Region(**region_model_dict()).save()
    provider_model.regions.connect(item)
    assert len(provider_model.regions.all()) == 2


def test_linked_identity_provider(
    provider_model: Provider, identity_provider_model: IdentityProvider
) -> None:
    assert provider_model.identity_providers.name
    assert provider_model.identity_providers.source
    assert isinstance(provider_model.identity_providers.source, Provider)
    assert provider_model.identity_providers.source.uid == provider_model.uid
    assert provider_model.identity_providers.definition
    assert (
        provider_model.identity_providers.definition["node_class"] == IdentityProvider
    )

    d = auth_method_dict()
    r = provider_model.identity_providers.connect(identity_provider_model, d)
    assert isinstance(r, AuthMethod)
    assert r.idp_name == d["idp_name"]
    assert r.protocol == d["protocol"]

    assert len(provider_model.identity_providers.all()) == 1
    identity_provider = provider_model.identity_providers.single()
    assert isinstance(identity_provider, IdentityProvider)
    assert identity_provider.uid == identity_provider_model.uid


def test_multiple_linked_identity_providers(provider_model: Provider) -> None:
    item = IdentityProvider(**identity_provider_model_dict()).save()
    provider_model.identity_providers.connect(item, auth_method_dict())
    item = IdentityProvider(**identity_provider_model_dict()).save()
    provider_model.identity_providers.connect(item, auth_method_dict())
    assert len(provider_model.identity_providers.all()) == 2
