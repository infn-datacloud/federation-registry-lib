from typing import Any
from unittest.mock import patch

import pytest
from neomodel import (
    AttemptedCardinalityViolation,
    CardinalityViolation,
    RelationshipManager,
)
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.flavor.models import Flavor
from fed_reg.image.models import Image
from fed_reg.network.models import Network
from fed_reg.project.models import Project
from fed_reg.provider.models import Provider
from fed_reg.sla.models import SLA
from tests.create_dict import (
    flavor_model_dict,
    image_model_dict,
    network_model_dict,
    project_model_dict,
    provider_model_dict,
    sla_model_dict,
)
from tests.utils import random_lower_string


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> tuple[str, str]:
        return key, random_lower_string()


def test_default_attr() -> None:
    d = project_model_dict()
    item = Project(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid")
    assert isinstance(item.sla, RelationshipManager)
    assert isinstance(item.provider, RelationshipManager)
    assert isinstance(item.quotas, RelationshipManager)
    assert isinstance(item.private_flavors, RelationshipManager)
    assert isinstance(item.private_images, RelationshipManager)
    assert isinstance(item.private_networks, RelationshipManager)


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(key: str, value: Any) -> None:
    d = project_model_dict()
    d[key] = value

    item = Project(**d)
    saved = item.save()

    assert saved.element_id_property
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(project_model: Project) -> None:
    with pytest.raises(CardinalityViolation):
        project_model.provider.all()
    with pytest.raises(CardinalityViolation):
        project_model.provider.single()


def test_optional_rel(project_model: Project) -> None:
    assert len(project_model.sla.all()) == 0
    assert project_model.sla.single() is None
    assert len(project_model.quotas.all()) == 0
    assert project_model.quotas.single() is None
    assert len(project_model.private_flavors.all()) == 0
    assert project_model.private_flavors.single() is None
    assert len(project_model.private_images.all()) == 0
    assert project_model.private_images.single() is None
    assert len(project_model.private_networks.all()) == 0
    assert project_model.private_networks.single() is None


def test_linked_flavor(project_model: Project, flavor_model: Flavor) -> None:
    assert project_model.private_flavors.name
    assert project_model.private_flavors.source
    assert isinstance(project_model.private_flavors.source, Project)
    assert project_model.private_flavors.source.uid == project_model.uid
    assert project_model.private_flavors.definition
    assert project_model.private_flavors.definition["node_class"] == Flavor

    r = project_model.private_flavors.connect(flavor_model)
    assert r is True

    assert len(project_model.private_flavors.all()) == 1
    project = project_model.private_flavors.single()
    assert isinstance(project, Flavor)
    assert project.uid == flavor_model.uid


def test_multiple_linked_flavors(project_model: Project) -> None:
    item = Flavor(**flavor_model_dict()).save()
    project_model.private_flavors.connect(item)
    item = Flavor(**flavor_model_dict()).save()
    project_model.private_flavors.connect(item)
    assert len(project_model.private_flavors.all()) == 2


def test_linked_image(project_model: Project, image_model: Image) -> None:
    assert project_model.private_images.name
    assert project_model.private_images.source
    assert isinstance(project_model.private_images.source, Project)
    assert project_model.private_images.source.uid == project_model.uid
    assert project_model.private_images.definition
    assert project_model.private_images.definition["node_class"] == Image

    r = project_model.private_images.connect(image_model)
    assert r is True

    assert len(project_model.private_images.all()) == 1
    project = project_model.private_images.single()
    assert isinstance(project, Image)
    assert project.uid == image_model.uid


def test_multiple_linked_images(project_model: Project) -> None:
    item = Image(**image_model_dict()).save()
    project_model.private_images.connect(item)
    item = Image(**image_model_dict()).save()
    project_model.private_images.connect(item)
    assert len(project_model.private_images.all()) == 2


def test_linked_network(project_model: Project, network_model: Network) -> None:
    assert project_model.private_networks.name
    assert project_model.private_networks.source
    assert isinstance(project_model.private_networks.source, Project)
    assert project_model.private_networks.source.uid == project_model.uid
    assert project_model.private_networks.definition
    assert project_model.private_networks.definition["node_class"] == Network

    r = project_model.private_networks.connect(network_model)
    assert r is True

    assert len(project_model.private_networks.all()) == 1
    project = project_model.private_networks.single()
    assert isinstance(project, Network)
    assert project.uid == network_model.uid


def test_multiple_linked_networks(project_model: Project) -> None:
    item = Network(**network_model_dict()).save()
    project_model.private_networks.connect(item)
    item = Network(**network_model_dict()).save()
    project_model.private_networks.connect(item)
    assert len(project_model.private_networks.all()) == 2


def test_linked_provider(project_model: Project, provider_model: Provider) -> None:
    assert project_model.provider.name
    assert project_model.provider.source
    assert isinstance(project_model.provider.source, Project)
    assert project_model.provider.source.uid == project_model.uid
    assert project_model.provider.definition
    assert project_model.provider.definition["node_class"] == Provider

    r = project_model.provider.connect(provider_model)
    assert r is True

    assert len(project_model.provider.all()) == 1
    provider = project_model.provider.single()
    assert isinstance(provider, Provider)
    assert provider.uid == provider_model.uid


def test_multiple_linked_provider(project_model: Project) -> None:
    item = Provider(**provider_model_dict()).save()
    project_model.provider.connect(item)
    item = Provider(**provider_model_dict()).save()
    with pytest.raises(AttemptedCardinalityViolation):
        project_model.provider.connect(item)

    with patch("neomodel.sync_.match.QueryBuilder._count", return_value=0):
        project_model.provider.connect(item)
        with pytest.raises(CardinalityViolation):
            project_model.provider.all()


def test_linked_sla(project_model: Project, sla_model: SLA) -> None:
    assert project_model.sla.name
    assert project_model.sla.source
    assert isinstance(project_model.sla.source, Project)
    assert project_model.sla.source.uid == project_model.uid
    assert project_model.sla.definition
    assert project_model.sla.definition["node_class"] == SLA

    r = project_model.sla.connect(sla_model)
    assert r is True

    assert len(project_model.sla.all()) == 1
    sla = project_model.sla.single()
    assert isinstance(sla, SLA)
    assert sla.uid == sla_model.uid


def test_multiple_linked_sla(project_model: Project) -> None:
    item = SLA(**sla_model_dict()).save()
    project_model.sla.connect(item)
    item = SLA(**sla_model_dict()).save()
    with pytest.raises(AttemptedCardinalityViolation):
        project_model.sla.connect(item)

    with patch("neomodel.sync_.match.QueryBuilder._count", return_value=0):
        project_model.sla.connect(item)
        with pytest.raises(CardinalityViolation):
            project_model.sla.all()


# TODO test public_flavors
# TODO test public_images
# TODO test public_networks
# ! Current tests does not check if flavor, image and network are privates or publics.
