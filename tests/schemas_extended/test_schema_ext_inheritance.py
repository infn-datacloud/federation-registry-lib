from pytest_cases import parametrize_with_cases

from fed_reg.models import BaseNodeRead, BaseReadPrivateExtended, BaseReadPublicExtended


@parametrize_with_cases("child, parent", has_tag="create")
def test_base(child, parent) -> None:
    assert issubclass(child, parent)


@parametrize_with_cases("child, parent", has_tag="read")
def test_read(child, parent) -> None:
    assert issubclass(child, BaseNodeRead)
    assert issubclass(child, BaseReadPrivateExtended)
    assert issubclass(child, parent)
    assert child.__config__.orm_mode


@parametrize_with_cases("child, parent", has_tag="read_public")
def test_read_public(child, parent) -> None:
    assert issubclass(child, BaseNodeRead)
    assert issubclass(child, BaseReadPublicExtended)
    assert issubclass(child, parent)
    assert child.__config__.orm_mode
