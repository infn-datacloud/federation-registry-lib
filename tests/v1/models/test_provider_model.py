from typing import Any

import pytest
from neomodel import DoesNotExist, RelationshipManager, RequiredProperty
from pytest_cases import parametrize_with_cases

from fedreg.auth_method.models import AuthMethod
from fedreg.identity_provider.models import IdentityProvider
from fedreg.image.models import Image
from fedreg.project.models import Project
from fedreg.provider.enum import ProviderStatus
from fedreg.provider.models import Provider
from fedreg.region.models import Region
from tests.v1.models.utils import (
    auth_method_model_dict,
    identity_provider_model_dict,
    project_model_dict,
    provider_model_dict,
    region_model_dict,
)


@parametrize_with_cases("data", has_tag=("dict", "valid"))
def test_provider_valid_attr(data: dict[str, Any]) -> None:
    """Test Provider mandatory and optional attributes."""
    item = Provider(**data)
    assert isinstance(item, Provider)
    assert item.uid is not None
    assert item.description == data.get("description", "")
    assert item.name == data.get("name")
    assert item.type == data.get("type")
    assert item.status is data.get("status", ProviderStatus.ACTIVE.value)
    assert item.is_public is data.get("is_public", False)
    assert item.support_emails == data.get("support_emails", [])

    saved = item.save()
    assert saved.element_id_property
    assert saved.uid == item.uid


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid"))
def test_provider_missing_mandatory_attr(data: dict[str, Any], attr: str) -> None:
    """Test Provider required attributes.

    Creating a model without required values raises a RequiredProperty error.
    """
    err_msg = f"property '{attr}' on objects of class {Provider.__name__}"
    with pytest.raises(RequiredProperty, match=err_msg):
        Provider(**data).save()


def test_rel_def(provider_model: Provider) -> None:
    """Test relationships definition."""
    assert isinstance(provider_model.projects, RelationshipManager)
    assert provider_model.projects.name
    assert provider_model.projects.source
    assert isinstance(provider_model.projects.source, Provider)
    assert provider_model.projects.source.uid == provider_model.uid
    assert provider_model.projects.definition
    assert provider_model.projects.definition["node_class"] == Project

    assert isinstance(provider_model.regions, RelationshipManager)
    assert provider_model.regions.name
    assert provider_model.regions.source
    assert isinstance(provider_model.regions.source, Provider)
    assert provider_model.regions.source.uid == provider_model.uid
    assert provider_model.regions.definition
    assert provider_model.regions.definition["node_class"] == Region

    assert isinstance(provider_model.identity_providers, RelationshipManager)
    assert provider_model.identity_providers.name
    assert provider_model.identity_providers.source
    assert isinstance(provider_model.identity_providers.source, Provider)
    assert provider_model.identity_providers.source.uid == provider_model.uid
    assert provider_model.identity_providers.definition
    assert (
        provider_model.identity_providers.definition["node_class"] == IdentityProvider
    )


def test_optional_rel(provider_model: Provider) -> None:
    """Test Provider optional relationships."""
    assert len(provider_model.identity_providers.all()) == 0
    assert provider_model.identity_providers.single() is None
    assert len(provider_model.projects.all()) == 0
    assert provider_model.projects.single() is None
    assert len(provider_model.regions.all()) == 0
    assert provider_model.regions.single() is None


def test_single_linked_project(
    provider_model: Provider, project_model: Project
) -> None:
    """Verify `projects` relationship works correctly.

    Connect a single Project to a Provider.
    """
    provider_model.projects.connect(project_model)

    assert len(provider_model.projects.all()) == 1
    project = provider_model.projects.single()
    assert isinstance(project, Project)
    assert project.uid == project_model.uid


def test_multiple_linked_projects(provider_model: Provider) -> None:
    """Verify `projects` relationship works correctly.

    Connect multiple Project to a Provider.
    """
    item = Project(**project_model_dict()).save()
    provider_model.projects.connect(item)
    item = Project(**project_model_dict()).save()
    provider_model.projects.connect(item)
    assert len(provider_model.projects.all()) == 2


def test_single_linked_region(provider_model: Provider, region_model: Region) -> None:
    """Verify `regions` relationship works correctly.

    Connect a single Region to a Provider.
    """
    provider_model.regions.connect(region_model)

    assert len(provider_model.regions.all()) == 1
    region = provider_model.regions.single()
    assert isinstance(region, Region)
    assert region.uid == region_model.uid


def test_multiple_linked_regions(provider_model: Provider) -> None:
    """Verify `regions` relationship works correctly.

    Connect multiple Region to a Provider.
    """
    item = Region(**region_model_dict()).save()
    provider_model.regions.connect(item)
    item = Region(**region_model_dict()).save()
    provider_model.regions.connect(item)
    assert len(provider_model.regions.all()) == 2


def test_single_linked_identity_provider(
    provider_model: Provider, identity_provider_model: IdentityProvider
) -> None:
    """Verify `identity_providers` relationship works correctly.

    Connect a single IdentityProvider to a Provider.
    """
    d = auth_method_model_dict()
    r = provider_model.identity_providers.connect(identity_provider_model, d)
    assert isinstance(r, AuthMethod)
    assert r.idp_name == d["idp_name"]
    assert r.protocol == d["protocol"]

    assert len(provider_model.identity_providers.all()) == 1
    identity_provider = provider_model.identity_providers.single()
    assert isinstance(identity_provider, IdentityProvider)
    assert identity_provider.uid == identity_provider_model.uid


def test_multiple_linked_identity_providers(provider_model: Provider) -> None:
    """Verify `identity_providers` relationship works correctly.

    Connect multiple IdentityProvider to a Provider.
    """
    item = IdentityProvider(**identity_provider_model_dict()).save()
    provider_model.identity_providers.connect(item, auth_method_model_dict())
    item = IdentityProvider(**identity_provider_model_dict()).save()
    provider_model.identity_providers.connect(item, auth_method_model_dict())
    assert len(provider_model.identity_providers.all()) == 2


def test_pre_delete_hook_remove_projects(provider_model: Provider) -> None:
    """Delete provider and all related projects."""
    item1 = Project(**project_model_dict()).save()
    provider_model.projects.connect(item1)
    item2 = Project(**project_model_dict()).save()
    provider_model.projects.connect(item2)

    assert provider_model.delete()
    assert provider_model.deleted
    with pytest.raises(DoesNotExist):
        item1.refresh()
    with pytest.raises(DoesNotExist):
        item2.refresh()


def test_pre_delete_hook_remove_regions(provider_model: Provider) -> None:
    """Delete provider and all related regions."""
    item1 = Region(**region_model_dict()).save()
    provider_model.regions.connect(item1)
    item2 = Region(**region_model_dict()).save()
    provider_model.regions.connect(item2)

    assert provider_model.delete()
    assert provider_model.deleted
    with pytest.raises(DoesNotExist):
        item1.refresh()
    with pytest.raises(DoesNotExist):
        item2.refresh()


def test_pre_delete_hook_dont_remove_idp(
    identity_provider_model: IdentityProvider,
) -> None:
    """IDP with multiple providers is not deleted when deleting one provider."""
    item1 = Provider(**provider_model_dict()).save()
    identity_provider_model.providers.connect(item1, auth_method_model_dict())
    item2 = Provider(**provider_model_dict()).save()
    identity_provider_model.providers.connect(item2, auth_method_model_dict())

    assert item1.delete()
    assert item1.deleted
    assert identity_provider_model.providers.single() == item2


@parametrize_with_cases("provider, tot_images", has_tag="images")
def test_provider_images(provider: Provider, tot_images: int) -> None:
    images = provider.images()
    assert len(images) == tot_images
    assert isinstance(images[0], Image)
