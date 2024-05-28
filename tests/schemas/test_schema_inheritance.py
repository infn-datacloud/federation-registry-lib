from pytest_cases import filters as ft
from pytest_cases import parametrize_with_cases

from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery, BaseNodeRead


@parametrize_with_cases("cls", has_tag="base_public")
def test_base_public(cls) -> None:
    assert issubclass(cls, BaseNode)


@parametrize_with_cases("child, parent", has_tag="base")
def test_base(child, parent) -> None:
    assert issubclass(child, parent)


@parametrize_with_cases(
    "child, parent", filter=ft.has_tag("create") | ft.has_tag("update")
)
def test_create_or_update(child, parent) -> None:
    assert issubclass(child, BaseNodeCreate)
    assert issubclass(child, parent)


@parametrize_with_cases("cls", has_tag="query")
def test_query(cls) -> None:
    assert issubclass(cls, BaseNodeQuery)


@parametrize_with_cases(
    "child, parent", filter=ft.has_tag("read") | ft.has_tag("read_public")
)
def test_read_public(child, parent) -> None:
    assert issubclass(child, BaseNodeRead)
    assert issubclass(child, parent)
    assert child.__config__.orm_mode
