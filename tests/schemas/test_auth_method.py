from typing import Any

import pytest
from pydantic import BaseModel
from pytest_cases import parametrize_with_cases

from fedreg.auth_method.models import AuthMethod
from fedreg.auth_method.schemas import AuthMethodRead, OsAuthMethodCreate
from fedreg.core import BaseNodeCreate


def test_classes_inheritance() -> None:
    """Test pydantic schema inheritance."""
    assert issubclass(OsAuthMethodCreate, BaseModel)

    assert issubclass(OsAuthMethodCreate, BaseNodeCreate)

    assert AuthMethodRead.__config__.orm_mode


@parametrize_with_cases("auth_method_cls", has_tag="class")
@parametrize_with_cases("data", has_tag=("dict", "valid"))
def test_base(
    auth_method_cls: type[OsAuthMethodCreate] | type[AuthMethodRead],
    data: dict[str, Any],
) -> None:
    """Test AuthMethod class' mandatory and optional attributes.

    Execute this test on AuthMethodBase, AuthMethodCreate and AuthMethodRead.
    """
    item = auth_method_cls(**data)
    assert item.idp_name == data.get("idp_name")
    assert item.protocol == data.get("protocol")


@parametrize_with_cases("model", has_tag="model")
def test_read_from_orm(model: AuthMethod) -> None:
    """Use the from_orm function of AuthMethodReadPublic to read data from an ORM."""
    item = AuthMethodRead.from_orm(model)
    assert item.idp_name == model.idp_name
    assert item.protocol == model.protocol


@parametrize_with_cases("auth_method_cls", has_tag="class")
@parametrize_with_cases("data, attr", has_tag=("dict", "invalid"))
def test_invalid(
    auth_method_cls: type[OsAuthMethodCreate] | type[AuthMethodRead],
    data: dict[str, Any],
    attr: str,
) -> None:
    """Test invalid attributes for base and create.

    Apply to AuthMethodBase, PrivateAuthMethodCreate and SharedAuthMethodCreate.
    """
    err_msg = rf"1 validation error for {auth_method_cls.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        auth_method_cls(**data)
