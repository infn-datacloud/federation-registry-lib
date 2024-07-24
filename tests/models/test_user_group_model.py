from unittest.mock import patch

import pytest
from neomodel import (
    AttemptedCardinalityViolation,
    CardinalityViolation,
    RelationshipManager,
)

from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.sla.models import SLA
from fed_reg.user_group.models import UserGroup
from tests.create_dict import (
    identity_provider_model_dict,
    sla_model_dict,
    user_group_model_dict,
)


def test_default_attr() -> None:
    d = user_group_model_dict()
    item = UserGroup(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert isinstance(item.identity_provider, RelationshipManager)
    assert isinstance(item.slas, RelationshipManager)


def test_required_rel(user_group_model: UserGroup) -> None:
    with pytest.raises(CardinalityViolation):
        user_group_model.identity_provider.all()
    with pytest.raises(CardinalityViolation):
        user_group_model.identity_provider.single()


def test_optional_rel(user_group_model: UserGroup) -> None:
    assert len(user_group_model.slas.all()) == 0
    assert user_group_model.slas.single() is None


def test_linked_sla(user_group_model: UserGroup, sla_model: SLA) -> None:
    assert user_group_model.slas.name
    assert user_group_model.slas.source
    assert isinstance(user_group_model.slas.source, UserGroup)
    assert user_group_model.slas.source.uid == user_group_model.uid
    assert user_group_model.slas.definition
    assert user_group_model.slas.definition["node_class"] == SLA

    r = user_group_model.slas.connect(sla_model)
    assert r is True

    assert len(user_group_model.slas.all()) == 1
    sla = user_group_model.slas.single()
    assert isinstance(sla, SLA)
    assert sla.uid == sla_model.uid


def test_multiple_linked_slas(user_group_model: UserGroup) -> None:
    item = SLA(**sla_model_dict()).save()
    user_group_model.slas.connect(item)
    item = SLA(**sla_model_dict()).save()
    user_group_model.slas.connect(item)
    assert len(user_group_model.slas.all()) == 2


def test_linked_identity_provider(
    user_group_model: UserGroup, identity_provider_model: IdentityProvider
) -> None:
    assert user_group_model.identity_provider.name
    assert user_group_model.identity_provider.source
    assert isinstance(user_group_model.identity_provider.source, UserGroup)
    assert user_group_model.identity_provider.source.uid == user_group_model.uid
    assert user_group_model.identity_provider.definition
    assert (
        user_group_model.identity_provider.definition["node_class"] == IdentityProvider
    )

    r = user_group_model.identity_provider.connect(identity_provider_model)
    assert r is True

    assert len(user_group_model.identity_provider.all()) == 1
    identity_provider = user_group_model.identity_provider.single()
    assert isinstance(identity_provider, IdentityProvider)
    assert identity_provider.uid == identity_provider_model.uid


def test_multiple_linked_identity_provider(user_group_model: UserGroup) -> None:
    item = IdentityProvider(**identity_provider_model_dict()).save()
    user_group_model.identity_provider.connect(item)
    item = IdentityProvider(**identity_provider_model_dict()).save()
    with pytest.raises(AttemptedCardinalityViolation):
        user_group_model.identity_provider.connect(item)

    with patch("neomodel.sync_.match.QueryBuilder._count", return_value=0):
        user_group_model.identity_provider.connect(item)
        with pytest.raises(CardinalityViolation):
            user_group_model.identity_provider.all()
