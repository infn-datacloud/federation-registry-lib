from random import randint
from typing import Any, Dict, Literal, Tuple
from unittest.mock import Mock, PropertyMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.flavor.models import Flavor
from tests.common.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "uuid"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description", "gpu_model", "gpu_vendor", "local_storage"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()

    @parametrize(key=["disk", "ram", "vcpus", "swap", "ephemeral", "gpus"])
    def case_int(self, key: str) -> Tuple[str, int]:
        return key, randint(0, 100)

    @parametrize(key=["is_public", "infiniband"])
    def case_bool(self, key: str) -> Tuple[str, Literal[True]]:
        return key, True


def flavor_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4().hex}


def test_default_attr() -> None:
    d = flavor_dict()
    item = Flavor(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid")
    assert item.disk == 0
    assert item.is_public is True
    assert item.ram == 0
    assert item.vcpus == 0
    assert item.swap == 0
    assert item.ephemeral == 0
    assert item.infiniband is False
    assert item.gpus == 0
    assert item.gpu_model is None
    assert item.gpu_vendor is None
    assert item.local_storage is None
    assert isinstance(item.projects, RelationshipManager)
    assert isinstance(item.services, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = flavor_dict()
    d[missing_attr] = None
    item = Flavor(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = flavor_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Flavor(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


# TODO test_invalid_relationships


# @patch("neomodel.core.db")
# def test_invalid_rel(mock_db: Mock) -> None:
#     d = {"name": random_lower_string(), "uuid": uuid4().hex}

#     db_version = "5"
#     type(mock_db).database_version = PropertyMock(return_value=db_version)
#     element_id = f"{db_version}:{uuid4().hex}:0"
#     mock_db.cypher_query.return_value = (
#         [[Node(..., element_id=element_id, id_=0, properties=d)]],
#         None,
#     )
#     item = Flavor(**d)
#     saved = item.save()
#     assert saved.id_element_property is not None
