from typing import Any, Union

import pytest
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.flavor.models import Flavor
from fed_reg.image.models import Image
from fed_reg.network.models import Network
from fed_reg.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota
from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
)
from tests.create_dict import (
    block_storage_quota_model_dict,
    compute_quota_model_dict,
    flavor_model_dict,
    image_model_dict,
    network_model_dict,
    network_quota_model_dict,
    service_model_dict,
)
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["type", "endpoint", "name"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> tuple[str, str]:
        return key, random_lower_string()


class CaseServiceModel:
    def case_block_storage_service(
        self, block_storage_service_model: BlockStorageService
    ) -> BlockStorageService:
        return block_storage_service_model

    def case_compute_service(
        self, compute_service_model: ComputeService
    ) -> ComputeService:
        return compute_service_model

    def case_identity_service(
        self, identity_service_model: IdentityService
    ) -> IdentityService:
        return identity_service_model

    def case_network_service(
        self, network_service_model: NetworkService
    ) -> NetworkService:
        return network_service_model


def test_block_storage_default_attr() -> None:
    d = service_model_dict()
    item = BlockStorageService(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.endpoint == d.get("endpoint")
    assert item.name == d.get("name")
    assert isinstance(item.region, RelationshipManager)
    assert isinstance(item.quotas, RelationshipManager)


def test_compute_default_attr() -> None:
    d = service_model_dict()
    item = ComputeService(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.endpoint == d.get("endpoint")
    assert item.name == d.get("name")
    assert isinstance(item.region, RelationshipManager)
    assert isinstance(item.flavors, RelationshipManager)
    assert isinstance(item.images, RelationshipManager)
    assert isinstance(item.quotas, RelationshipManager)


def test_identity_default_attr() -> None:
    d = service_model_dict()
    item = IdentityService(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.endpoint == d.get("endpoint")
    assert item.name == d.get("name")
    assert isinstance(item.region, RelationshipManager)


def test_network_default_attr() -> None:
    d = service_model_dict()
    item = NetworkService(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.endpoint == d.get("endpoint")
    assert item.name == d.get("name")
    assert isinstance(item.region, RelationshipManager)
    assert isinstance(item.networks, RelationshipManager)
    assert isinstance(item.quotas, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_block_storage_missing_attr(missing_attr: str) -> None:
    d = service_model_dict()
    d[missing_attr] = None
    item = BlockStorageService(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_compute_missing_attr(missing_attr: str) -> None:
    d = service_model_dict()
    d[missing_attr] = None
    item = ComputeService(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_identity_missing_attr(missing_attr: str) -> None:
    d = service_model_dict()
    d[missing_attr] = None
    item = IdentityService(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_network_missing_attr(missing_attr: str) -> None:
    d = service_model_dict()
    d[missing_attr] = None
    item = NetworkService(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_block_storage_attr(key: str, value: Any) -> None:
    d = service_model_dict()
    d[key] = value

    item = BlockStorageService(**d)
    saved = item.save()

    assert saved.element_id_property
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_compute_attr(key: str, value: Any) -> None:
    d = service_model_dict()
    d[key] = value

    item = ComputeService(**d)
    saved = item.save()

    assert saved.element_id_property
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_identity_attr(key: str, value: Any) -> None:
    d = service_model_dict()
    d[key] = value

    item = IdentityService(**d)
    saved = item.save()

    assert saved.element_id_property
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_network_attr(key: str, value: Any) -> None:
    d = service_model_dict()
    d[key] = value

    item = NetworkService(**d)
    saved = item.save()

    assert saved.element_id_property
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@parametrize_with_cases("service_model", cases=CaseServiceModel)
def test_required_rel(
    service_model: Union[
        BlockStorageService, ComputeService, IdentityService, NetworkService
    ],
) -> None:
    with pytest.raises(CardinalityViolation):
        service_model.region.all()
    with pytest.raises(CardinalityViolation):
        service_model.region.single()


def test_block_storage_optional_rel(
    block_storage_service_model: BlockStorageService,
) -> None:
    assert len(block_storage_service_model.quotas.all()) == 0
    assert block_storage_service_model.quotas.single() is None


def test_compute_optional_rel(compute_service_model: ComputeService) -> None:
    assert len(compute_service_model.quotas.all()) == 0
    assert compute_service_model.quotas.single() is None
    assert len(compute_service_model.flavors.all()) == 0
    assert compute_service_model.flavors.single() is None
    assert len(compute_service_model.images.all()) == 0
    assert compute_service_model.images.single() is None


def test_network_optional_rel(network_service_model: NetworkService) -> None:
    assert len(network_service_model.quotas.all()) == 0
    assert network_service_model.quotas.single() is None
    assert len(network_service_model.networks.all()) == 0
    assert network_service_model.networks.single() is None


def test_linked_block_storage_quota(
    block_storage_service_model: BlockStorageService,
    block_storage_quota_model: BlockStorageQuota,
) -> None:
    assert block_storage_service_model.quotas.name
    assert block_storage_service_model.quotas.source
    assert isinstance(block_storage_service_model.quotas.source, BlockStorageService)
    assert (
        block_storage_service_model.quotas.source.uid == block_storage_service_model.uid
    )
    assert block_storage_service_model.quotas.definition
    assert (
        block_storage_service_model.quotas.definition["node_class"] == BlockStorageQuota
    )

    r = block_storage_service_model.quotas.connect(block_storage_quota_model)
    assert r is True

    assert len(block_storage_service_model.quotas.all()) == 1
    quotas = block_storage_service_model.quotas.single()
    assert isinstance(quotas, BlockStorageQuota)
    assert quotas.uid == block_storage_quota_model.uid


def test_multiple_linked_block_storage_quotas(
    block_storage_service_model: BlockStorageService,
) -> None:
    item = BlockStorageQuota(**block_storage_quota_model_dict()).save()
    block_storage_service_model.quotas.connect(item)
    item = BlockStorageQuota(**block_storage_quota_model_dict()).save()
    block_storage_service_model.quotas.connect(item)
    assert len(block_storage_service_model.quotas.all()) == 2


def test_linked_compute_quota(
    compute_service_model: ComputeService, compute_quota_model: ComputeQuota
) -> None:
    assert compute_service_model.quotas.name
    assert compute_service_model.quotas.source
    assert isinstance(compute_service_model.quotas.source, ComputeService)
    assert compute_service_model.quotas.source.uid == compute_service_model.uid
    assert compute_service_model.quotas.definition
    assert compute_service_model.quotas.definition["node_class"] == ComputeQuota

    r = compute_service_model.quotas.connect(compute_quota_model)
    assert r is True

    assert len(compute_service_model.quotas.all()) == 1
    quotas = compute_service_model.quotas.single()
    assert isinstance(quotas, ComputeQuota)
    assert quotas.uid == compute_quota_model.uid


def test_multiple_linked_compute_quotas(compute_service_model: ComputeService) -> None:
    item = ComputeQuota(**compute_quota_model_dict()).save()
    compute_service_model.quotas.connect(item)
    item = ComputeQuota(**compute_quota_model_dict()).save()
    compute_service_model.quotas.connect(item)
    assert len(compute_service_model.quotas.all()) == 2


def test_linked_flavor(
    compute_service_model: ComputeService, flavor_model: Flavor
) -> None:
    assert compute_service_model.flavors.name
    assert compute_service_model.flavors.source
    assert isinstance(compute_service_model.flavors.source, ComputeService)
    assert compute_service_model.flavors.source.uid == compute_service_model.uid
    assert compute_service_model.flavors.definition
    assert compute_service_model.flavors.definition["node_class"] == Flavor

    r = compute_service_model.flavors.connect(flavor_model)
    assert r is True

    assert len(compute_service_model.flavors.all()) == 1
    flavors = compute_service_model.flavors.single()
    assert isinstance(flavors, Flavor)
    assert flavors.uid == flavor_model.uid


def test_multiple_linked_flavors(compute_service_model: ComputeService) -> None:
    item = Flavor(**flavor_model_dict()).save()
    compute_service_model.flavors.connect(item)
    item = Flavor(**flavor_model_dict()).save()
    compute_service_model.flavors.connect(item)
    assert len(compute_service_model.flavors.all()) == 2


def test_linked_image(
    compute_service_model: ComputeService, image_model: Image
) -> None:
    assert compute_service_model.images.name
    assert compute_service_model.images.source
    assert isinstance(compute_service_model.images.source, ComputeService)
    assert compute_service_model.images.source.uid == compute_service_model.uid
    assert compute_service_model.images.definition
    assert compute_service_model.images.definition["node_class"] == Image

    r = compute_service_model.images.connect(image_model)
    assert r is True

    assert len(compute_service_model.images.all()) == 1
    images = compute_service_model.images.single()
    assert isinstance(images, Image)
    assert images.uid == image_model.uid


def test_multiple_linked_images(compute_service_model: ComputeService) -> None:
    item = Image(**image_model_dict()).save()
    compute_service_model.images.connect(item)
    item = Image(**image_model_dict()).save()
    compute_service_model.images.connect(item)
    assert len(compute_service_model.images.all()) == 2


def test_linked_network_quota(
    network_service_model: NetworkService, network_quota_model: NetworkQuota
) -> None:
    assert network_service_model.quotas.name
    assert network_service_model.quotas.source
    assert isinstance(network_service_model.quotas.source, NetworkService)
    assert network_service_model.quotas.source.uid == network_service_model.uid
    assert network_service_model.quotas.definition
    assert network_service_model.quotas.definition["node_class"] == NetworkQuota

    r = network_service_model.quotas.connect(network_quota_model)
    assert r is True

    assert len(network_service_model.quotas.all()) == 1
    quotas = network_service_model.quotas.single()
    assert isinstance(quotas, NetworkQuota)
    assert quotas.uid == network_quota_model.uid


def test_multiple_linked_network_quotas(network_service_model: NetworkService) -> None:
    item = NetworkQuota(**network_quota_model_dict()).save()
    network_service_model.quotas.connect(item)
    item = NetworkQuota(**network_quota_model_dict()).save()
    network_service_model.quotas.connect(item)
    assert len(network_service_model.quotas.all()) == 2


def test_linked_network(
    network_service_model: NetworkService, network_model: Network
) -> None:
    assert network_service_model.networks.name
    assert network_service_model.networks.source
    assert isinstance(network_service_model.networks.source, NetworkService)
    assert network_service_model.networks.source.uid == network_service_model.uid
    assert network_service_model.networks.definition
    assert network_service_model.networks.definition["node_class"] == Network

    r = network_service_model.networks.connect(network_model)
    assert r is True

    assert len(network_service_model.networks.all()) == 1
    networks = network_service_model.networks.single()
    assert isinstance(networks, Network)
    assert networks.uid == network_model.uid


def test_multiple_linked_networks(network_service_model: NetworkService) -> None:
    item = Network(**network_model_dict()).save()
    network_service_model.networks.connect(item)
    item = Network(**network_model_dict()).save()
    network_service_model.networks.connect(item)
    assert len(network_service_model.networks.all()) == 2
