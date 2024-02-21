from typing import Any, Tuple
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import (
    AttemptedCardinalityViolation,
    CardinalityViolation,
    RelationshipManager,
    RequiredProperty,
)
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.flavor.models import Flavor
from fed_reg.image.models import Image
from fed_reg.network.models import Network
from fed_reg.project.models import Project
from fed_reg.provider.models import Provider
from fed_reg.sla.models import SLA
from tests.create_dict import project_dict
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "uuid"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()


def test_default_attr() -> None:
    d = project_dict()
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


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = project_dict()
    d[missing_attr] = None
    item = Project(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = project_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Project(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(db_match: MagicMock, project_model: Project) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        project_model.provider.all()
    with pytest.raises(CardinalityViolation):
        project_model.provider.single()


def test_optional_rel(db_match: MagicMock, project_model: Project) -> None:
    db_match.cypher_query.return_value = ([], None)
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


def test_linked_flavor(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    project_model: Project,
    flavor_model: Flavor,
) -> None:
    assert project_model.private_flavors.name
    assert project_model.private_flavors.source
    assert isinstance(project_model.private_flavors.source, Project)
    assert project_model.private_flavors.source.uid == project_model.uid
    assert project_model.private_flavors.definition
    assert project_model.private_flavors.definition["node_class"] == Flavor

    r = project_model.private_flavors.connect(flavor_model)
    assert r is True

    db_match.cypher_query.return_value = ([[flavor_model]], ["projects_r1"])
    assert len(project_model.private_flavors.all()) == 1
    project = project_model.private_flavors.single()
    assert isinstance(project, Flavor)
    assert project.uid == flavor_model.uid


def test_multiple_linked_flavors(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    flavor_model: Flavor,
    project_model: Project,
) -> None:
    db_match.cypher_query.return_value = (
        [[flavor_model], [flavor_model]],
        ["projects_r1", "projects_r2"],
    )
    assert len(project_model.private_flavors.all()) == 2


def test_linked_image(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    project_model: Project,
    image_model: Image,
) -> None:
    assert project_model.private_images.name
    assert project_model.private_images.source
    assert isinstance(project_model.private_images.source, Project)
    assert project_model.private_images.source.uid == project_model.uid
    assert project_model.private_images.definition
    assert project_model.private_images.definition["node_class"] == Image

    r = project_model.private_images.connect(image_model)
    assert r is True

    db_match.cypher_query.return_value = ([[image_model]], ["projects_r1"])
    assert len(project_model.private_images.all()) == 1
    project = project_model.private_images.single()
    assert isinstance(project, Image)
    assert project.uid == image_model.uid


def test_multiple_linked_images(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    image_model: Image,
    project_model: Project,
) -> None:
    db_match.cypher_query.return_value = (
        [[image_model], [image_model]],
        ["projects_r1", "projects_r2"],
    )
    assert len(project_model.private_images.all()) == 2


def test_linked_network(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    project_model: Project,
    network_model: Network,
) -> None:
    assert project_model.private_networks.name
    assert project_model.private_networks.source
    assert isinstance(project_model.private_networks.source, Project)
    assert project_model.private_networks.source.uid == project_model.uid
    assert project_model.private_networks.definition
    assert project_model.private_networks.definition["node_class"] == Network

    r = project_model.private_networks.connect(network_model)
    assert r is True

    db_match.cypher_query.return_value = ([[network_model]], ["projects_r1"])
    assert len(project_model.private_networks.all()) == 1
    project = project_model.private_networks.single()
    assert isinstance(project, Network)
    assert project.uid == network_model.uid


def test_multiple_linked_networks(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    network_model: Network,
    project_model: Project,
) -> None:
    db_match.cypher_query.return_value = (
        [[network_model], [network_model]],
        ["projects_r1", "projects_r2"],
    )
    assert len(project_model.private_networks.all()) == 2


@patch("neomodel.match.QueryBuilder._count", return_value=0)
def test_linked_provider(
    mock_count: MagicMock,
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    project_model: Project,
    provider_model: Provider,
) -> None:
    assert project_model.provider.name
    assert project_model.provider.source
    assert isinstance(project_model.provider.source, Project)
    assert project_model.provider.source.uid == project_model.uid
    assert project_model.provider.definition
    assert project_model.provider.definition["node_class"] == Provider

    r = project_model.provider.connect(provider_model)
    assert r is True

    db_match.cypher_query.return_value = ([[provider_model]], ["provider_r1"])
    assert len(project_model.provider.all()) == 1
    provider = project_model.provider.single()
    assert isinstance(provider, Provider)
    assert provider.uid == provider_model.uid


def test_multiple_linked_provider(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    project_model: Project,
    provider_model: Provider,
) -> None:
    with patch("neomodel.match.QueryBuilder._count") as mock_count:
        mock_count.return_value = 1
        with pytest.raises(AttemptedCardinalityViolation):
            project_model.provider.connect(provider_model)

    db_match.cypher_query.return_value = (
        [[provider_model], [provider_model]],
        ["provider_r1", "provider_r2"],
    )
    with pytest.raises(CardinalityViolation):
        project_model.provider.all()


@patch("neomodel.match.QueryBuilder._count", return_value=0)
def test_linked_sla(
    mock_count: MagicMock,
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    project_model: Project,
    sla_model: SLA,
) -> None:
    assert project_model.sla.name
    assert project_model.sla.source
    assert isinstance(project_model.sla.source, Project)
    assert project_model.sla.source.uid == project_model.uid
    assert project_model.sla.definition
    assert project_model.sla.definition["node_class"] == SLA

    r = project_model.sla.connect(sla_model)
    assert r is True

    db_match.cypher_query.return_value = ([[sla_model]], ["sla_r1"])
    assert len(project_model.sla.all()) == 1
    sla = project_model.sla.single()
    assert isinstance(sla, SLA)
    assert sla.uid == sla_model.uid


def test_multiple_linked_sla(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    project_model: Project,
    sla_model: SLA,
) -> None:
    with patch("neomodel.match.QueryBuilder._count") as mock_count:
        mock_count.return_value = 1
        with pytest.raises(AttemptedCardinalityViolation):
            project_model.sla.connect(sla_model)

    db_match.cypher_query.return_value = (
        [[sla_model], [sla_model]],
        ["sla_r1", "sla_r2"],
    )
    with pytest.raises(CardinalityViolation):
        project_model.sla.all()


# TODO test public_flavors
# TODO test public_images
# TODO test public_networks
# ! Current tests does not check if flavor, image and network are privates or publics.
