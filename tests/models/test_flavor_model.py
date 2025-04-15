from typing import Any

import pytest
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize_with_cases

from fedreg.flavor.models import Flavor, PrivateFlavor, SharedFlavor
from fedreg.project.models import Project
from fedreg.service.models import ComputeService
from tests.models.utils import project_model_dict


@parametrize_with_cases("flavor_cls", has_tag=("class", "derived"))
def test_flavor_inheritance(
    flavor_cls: type[PrivateFlavor] | type[SharedFlavor],
) -> None:
    """Test PrivateFlavor and SharedFlavor inherits from Flavor."""
    assert issubclass(flavor_cls, Flavor)


@parametrize_with_cases("flavor_cls", has_tag="class")
@parametrize_with_cases("data", has_tag=("dict", "valid"))
def test_flavor_valid_attr(
    flavor_cls: type[Flavor] | type[PrivateFlavor] | type[SharedFlavor],
    data: dict[str, Any],
) -> None:
    """Test Flavor mandatory and optional attributes.

    Execute this test on Flavor, PrivateFlavor and SharedFlavor.
    """
    item = flavor_cls(**data)
    assert isinstance(item, flavor_cls)
    assert item.uid is not None
    assert item.description == data.get("description", "")
    assert item.name == data.get("name")
    assert item.uuid == data.get("uuid")
    assert item.disk == data.get("disk", 0)
    assert item.ram == data.get("ram", 0)
    assert item.vcpus == data.get("vcpus", 0)
    assert item.swap == data.get("swap", 0)
    assert item.ephemeral == data.get("ephemeral", 0)
    assert item.infiniband is data.get("infiniband", False)
    assert item.gpus == data.get("gpus", 0)
    assert item.gpu_model is data.get("gpu_model", None)
    assert item.gpu_vendor is data.get("gpu_vendor", None)
    assert item.local_storage is data.get("local_storage", None)

    if flavor_cls == SharedFlavor:
        assert item.is_shared
    if flavor_cls == PrivateFlavor:
        assert not item.is_shared

    saved = item.save()
    assert saved.element_id_property
    assert saved.uid == item.uid


@parametrize_with_cases("flavor_cls", has_tag="class")
@parametrize_with_cases("data, attr", has_tag=("dict", "invalid"))
def test_flavor_missing_mandatory_attr(
    flavor_cls: type[Flavor] | type[PrivateFlavor] | type[SharedFlavor],
    data: dict[str, Any],
    attr: str,
) -> None:
    """Creating a model without required values raises a RequiredProperty error.

    Execute this test on Flavor, PrivateFlavor and SharedFlavor.
    """
    err_msg = f"property '{attr}' on objects of class {flavor_cls.__name__}"
    with pytest.raises(RequiredProperty, match=err_msg):
        flavor_cls(**data).save()


@parametrize_with_cases("flavor_model", has_tag="model")
def test_rel_def(flavor_model: Flavor | PrivateFlavor | SharedFlavor) -> None:
    """Test relationships definition.

    Execute this test on Flavor, PrivateFlavor and SharedFlavor.
    """
    assert isinstance(flavor_model.service, RelationshipManager)
    assert flavor_model.service.name
    assert flavor_model.service.source
    assert isinstance(flavor_model.service.source, type(flavor_model))
    assert flavor_model.service.source.uid == flavor_model.uid
    assert flavor_model.service.definition
    assert flavor_model.service.definition["node_class"] == ComputeService

    if isinstance(flavor_model, PrivateFlavor):
        assert isinstance(flavor_model.projects, RelationshipManager)
        assert flavor_model.projects.name
        assert flavor_model.projects.source
        assert isinstance(flavor_model.projects.source, PrivateFlavor)
        assert flavor_model.projects.source.uid == flavor_model.uid
        assert flavor_model.projects.definition
        assert flavor_model.projects.definition["node_class"] == Project


@parametrize_with_cases("flavor_model", has_tag="model")
def test_required_rel(flavor_model: Flavor | PrivateFlavor | SharedFlavor) -> None:
    """Test Flavor required relationships.

    A model without required relationships can exist but when querying those values, it
    raises a CardinalityViolation error.
    Execute this test on Flavor, PrivateFlavor and SharedFlavor.
    """
    with pytest.raises(CardinalityViolation):
        flavor_model.service.all()
    with pytest.raises(CardinalityViolation):
        flavor_model.service.single()

    if isinstance(flavor_model, PrivateFlavor):
        with pytest.raises(CardinalityViolation):
            flavor_model.projects.all()
        with pytest.raises(CardinalityViolation):
            flavor_model.projects.single()


@parametrize_with_cases("flavor_model", has_tag="model")
def test_single_linked_service(
    flavor_model: Flavor | PrivateFlavor | SharedFlavor,
    compute_service_model: ComputeService,
) -> None:
    """Verify `service` relationship works correctly.

    Connect a single ComputeService to a Flavor.
    Execute this test on Flavor, PrivateFlavor and SharedFlavor.
    """
    flavor_model.service.connect(compute_service_model)

    assert len(flavor_model.service.all()) == 1
    service = flavor_model.service.single()
    assert isinstance(service, ComputeService)
    assert service.uid == compute_service_model.uid


def test_single_linked_project(
    private_flavor_model: PrivateFlavor, project_model: Project
) -> None:
    """Verify `projects` relationship works correctly.

    Connect a single Project to a PrivateFlavor.
    """
    private_flavor_model.projects.connect(project_model)

    assert len(private_flavor_model.projects.all()) == 1
    project = private_flavor_model.projects.single()
    assert isinstance(project, Project)
    assert project.uid == project_model.uid


def test_multiple_linked_projects(private_flavor_model: PrivateFlavor) -> None:
    """Verify `projects` relationship works correctly.

    Connect a multiple Project to a PrivateFlavor.
    """
    item = Project(**project_model_dict()).save()
    private_flavor_model.projects.connect(item)
    item = Project(**project_model_dict()).save()
    private_flavor_model.projects.connect(item)
    assert len(private_flavor_model.projects.all()) == 2
