import pytest
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.provider.crud import provider_mng
from fed_reg.provider.models import Provider
from fed_reg.provider.schemas_extended import ProviderCreateExtended
from tests.create_dict import provider_model_dict


class CaseAttr:
    def case_none(self) -> None:
        return None

    @parametrize(
        value=[
            "uid",
            "description",
            "name",
            "type",
            "status",
            "is_public",
            "support_emails",
        ]
    )
    def case_key(self, value: str) -> str:
        return value


class CaseProvider:
    @parametrize(len=[1, 2])
    def case_provider(self, len: int) -> list[Provider]:
        providers = []
        for _ in range(len):
            providers.append(Provider(**provider_model_dict()).save())
        return providers


def test_create(provider_create_ext_schema: ProviderCreateExtended) -> None:
    item = provider_mng.create(obj_in=provider_create_ext_schema)
    assert isinstance(item, Provider)
    assert item.uid is not None
    assert item.description == provider_create_ext_schema.description
    assert item.name == provider_create_ext_schema.name
    assert item.type == provider_create_ext_schema.type
    assert item.is_public == provider_create_ext_schema.is_public
    assert item.status == provider_create_ext_schema.status
    assert item.support_emails == provider_create_ext_schema.support_emails
    assert len(item.identity_providers) == len(
        provider_create_ext_schema.identity_providers
    )
    assert len(item.projects) == len(provider_create_ext_schema.projects)
    assert len(item.regions) == len(provider_create_ext_schema.regions)


@parametrize_with_cases("providers", cases=CaseProvider)
def test_read_multi(providers: Provider) -> None:
    items = provider_mng.get_multi()
    assert len(items) == len(providers)


def test_read_empty_list() -> None:
    items = provider_mng.get_multi()
    assert len(items) == 0


@parametrize_with_cases("attr", cases=CaseAttr)
def test_read_single(provider_model: Provider, attr: str) -> None:
    kwargs = {attr: provider_model.__getattribute__(attr)} if attr else {}
    item = provider_mng.get(**kwargs)
    assert isinstance(item, Provider)
    assert item.uid == provider_model.uid


def test_read_none() -> None:
    assert not provider_mng.get()


def test_delete(provider_model: Provider) -> None:
    assert provider_mng.remove(db_obj=provider_model)
    assert provider_model.deleted


def test_delete_not_existing(provider_model: Provider) -> None:
    assert provider_mng.remove(db_obj=provider_model)
    with pytest.raises(ValueError):
        provider_mng.remove(db_obj=provider_model)
