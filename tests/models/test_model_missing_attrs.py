import pytest
from neomodel import RequiredProperty, StructuredNode
from pytest_cases import parametrize_with_cases


@parametrize_with_cases("data, model, attr")
def test_missing_attr(data: dict, model: type[StructuredNode], attr: str) -> None:
    data[attr] = None
    item = model(**data)
    with pytest.raises(RequiredProperty):
        item.save()
