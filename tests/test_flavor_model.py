from uuid import uuid4

import pytest
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.flavor.models import Flavor
from tests.common.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "uuid"])
    def case_missing(self, value: str) -> str:
        return value


def test_default_attr() -> None:
    d = {"name": random_lower_string(), "uuid": uuid4().hex}
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
    d = {
        "name": None if missing_attr == "name" else random_lower_string(),
        "uuid": None if missing_attr == "uuid" else uuid4().hex,
    }
    item = Flavor(**d)
    with pytest.raises(RequiredProperty):
        item.save()


# TODO test_invalid_relationships

# @patch("neomodel.core.db")
# def test_invalid_rel(mock_db: Mock) -> None:
#     d = {"name": random_lower_string(), "uuid": uuid4().hex}

#     db_version = "5"
#     type(mock_db).database_version = PropertyMock(return_value=db_version)
#     element_id = item"{db_version}:{uuid4().hex}:0"
#     mock_db.cypher_query.return_value = (
#         [[Node(..., element_id=element_id, id_=0, properties=d)]],
#         None,
#     )
#     item = Flavor(**d)
#     item.save()
