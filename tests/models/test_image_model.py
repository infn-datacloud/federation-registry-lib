from typing import Any, Literal

import pytest
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.image.models import Image
from fed_reg.project.models import Project
from fed_reg.service.models import ComputeService
from tests.create_dict import (
    compute_service_model_dict,
    image_model_dict,
    project_model_dict,
)
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "uuid"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(
        key=[
            "description",
            "os_type",
            "os_distro",
            "os_version",
            "architecture",
            "kernel_id",
        ]
    )
    def case_str(self, key: str) -> tuple[str, str]:
        return key, random_lower_string()

    @parametrize(key=["cuda_support", "gpu_driver", "is_public"])
    def case_bool(self, key: str) -> tuple[str, Literal[True]]:
        return key, True

    @parametrize(key=["empty", "full"])
    def case_list_str(self, key: str) -> tuple[str, list[str]]:
        if key == "empty":
            return key, []
        return key, [random_lower_string()]


def test_default_attr() -> None:
    d = image_model_dict()
    item = Image(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid")
    assert item.is_public is True
    assert item.os_type is None
    assert item.os_distro is None
    assert item.os_version is None
    assert item.architecture is None
    assert item.kernel_id is None
    assert item.cuda_support is False
    assert item.gpu_driver is False
    assert item.tags == []
    assert isinstance(item.projects, RelationshipManager)
    assert isinstance(item.services, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = image_model_dict()
    d[missing_attr] = None
    item = Image(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(key: str, value: Any) -> None:
    d = image_model_dict()
    d[key] = value

    item = Image(**d)
    saved = item.save()

    assert saved.element_id_property
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(image_model: Image) -> None:
    with pytest.raises(CardinalityViolation):
        image_model.services.all()
    with pytest.raises(CardinalityViolation):
        image_model.services.single()


def test_optional_rel(image_model: Image) -> None:
    assert len(image_model.projects.all()) == 0
    assert image_model.projects.single() is None


def test_linked_project(image_model: Image, project_model: Project) -> None:
    assert image_model.projects.name
    assert image_model.projects.source
    assert isinstance(image_model.projects.source, Image)
    assert image_model.projects.source.uid == image_model.uid
    assert image_model.projects.definition
    assert image_model.projects.definition["node_class"] == Project

    r = image_model.projects.connect(project_model)
    assert r is True

    assert len(image_model.projects.all()) == 1
    project = image_model.projects.single()
    assert isinstance(project, Project)
    assert project.uid == project_model.uid


def test_multiple_linked_projects(image_model: Image) -> None:
    item = Project(**project_model_dict()).save()
    image_model.projects.connect(item)
    item = Project(**project_model_dict()).save()
    image_model.projects.connect(item)
    assert len(image_model.projects.all()) == 2


def test_linked_service(
    image_model: Image, compute_service_model: ComputeService
) -> None:
    assert image_model.services.name
    assert image_model.services.source
    assert isinstance(image_model.services.source, Image)
    assert image_model.services.source.uid == image_model.uid
    assert image_model.services.definition
    assert image_model.services.definition["node_class"] == ComputeService

    r = image_model.services.connect(compute_service_model)
    assert r is True

    assert len(image_model.services.all()) == 1
    service = image_model.services.single()
    assert isinstance(service, ComputeService)
    assert service.uid == compute_service_model.uid


def test_multiple_linked_services(image_model: Image) -> None:
    item = ComputeService(**compute_service_model_dict()).save()
    image_model.services.connect(item)
    item = ComputeService(**compute_service_model_dict()).save()
    image_model.services.connect(item)
    assert len(image_model.services.all()) == 2
