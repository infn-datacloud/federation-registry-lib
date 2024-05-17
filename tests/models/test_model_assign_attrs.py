from typing import Any

from neomodel import StructuredNode
from pytest_cases import parametrize_with_cases


@parametrize_with_cases("data, model, attr, value")
def test_assign_attr(
    data: dict, model: type[StructuredNode], attr: str, value: Any
) -> None:
    data[attr] = value
    item = model(**data)
    saved = item.save()
    assert saved.element_id_property
    assert saved.uid == item.uid
    assert saved.__getattribute__(attr) == value
