from random import randint
from unittest.mock import MagicMock
from uuid import uuid4

from neo4j.graph import Node, Relationship

from fed_reg.flavor.models import Flavor
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.image.models import Image
from fed_reg.location.models import Location
from fed_reg.network.models import Network
from fed_reg.project.models import Project
from fed_reg.provider.models import Provider
from fed_reg.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota
from fed_reg.region.models import Region
from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
)
from fed_reg.sla.models import SLA
from fed_reg.user_group.models import UserGroup
from tests.create_dict import (
    auth_method_dict,
    block_storage_quota_model_dict,
    block_storage_service_model_dict,
    compute_quota_model_dict,
    compute_service_model_dict,
    flavor_model_dict,
    identity_provider_model_dict,
    identity_service_model_dict,
    image_model_dict,
    location_model_dict,
    network_model_dict,
    network_quota_model_dict,
    network_service_model_dict,
    project_model_dict,
    provider_model_dict,
    region_model_dict,
    sla_model_dict,
    user_group_model_dict,
)

FLAVOR_ID = 100
IDENTITY_PROVIDER_ID = 200
IMAGE_ID = 300
LOCATION_ID = 400
NETWORK_ID = 500
PROJECT_ID = 600
PROVIDER_ID = 700
BLOCK_STORAGE_QUOTA_ID = 800
COMPUTE_QUOTA_ID = 900
NETWORK_QUOTA_ID = 1000
REGION_ID = 1100
BLOCK_STORAGE_SERVICE_ID = 1200
COMPUTE_SERVICE_ID = 1300
IDENTITY_SERVICE_ID = 1400
NETWORK_SERVICE_ID = 1500
SLA_ID = 1600
USER_GROUP_ID = 1700

DB_VERSION = "5"


def flavor_neomodel(db: MagicMock) -> Flavor:
    d = flavor_model_dict()
    item_id = FLAVOR_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return Flavor(**d).save()


def identity_provider_neomodel(db: MagicMock) -> IdentityProvider:
    d = identity_provider_model_dict()
    item_id = IDENTITY_PROVIDER_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return IdentityProvider(**d).save()


def image_neomodel(db: MagicMock) -> Image:
    d = image_model_dict()
    item_id = IMAGE_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return Image(**d).save()


def location_neomodel(db: MagicMock) -> Location:
    d = location_model_dict()
    item_id = LOCATION_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return Location(**d).save()


def network_neomodel(db: MagicMock) -> Network:
    d = network_model_dict()
    item_id = NETWORK_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return Network(**d).save()


def project_neomodel(db: MagicMock) -> Project:
    d = project_model_dict()
    item_id = PROJECT_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return Project(**d).save()


def provider_neomodel(db: MagicMock) -> Provider:
    d = provider_model_dict()
    item_id = PROVIDER_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return Provider(**d).save()


def block_storage_quota_neomodel(db: MagicMock) -> BlockStorageQuota:
    d = block_storage_quota_model_dict()
    item_id = BLOCK_STORAGE_QUOTA_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return BlockStorageQuota(**d).save()


def compute_quota_neomodel(db: MagicMock) -> ComputeQuota:
    d = compute_quota_model_dict()
    item_id = COMPUTE_QUOTA_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return ComputeQuota(**d).save()


def network_quota_neomodel(db: MagicMock) -> NetworkQuota:
    d = network_quota_model_dict()
    item_id = NETWORK_QUOTA_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return NetworkQuota(**d).save()


def region_neomodel(db: MagicMock) -> Region:
    d = region_model_dict()
    item_id = REGION_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return Region(**d).save()


def block_storage_service_neomodel(db: MagicMock) -> BlockStorageService:
    d = block_storage_service_model_dict()
    item_id = BLOCK_STORAGE_SERVICE_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return BlockStorageService(**d).save()


def compute_service_neomodel(db: MagicMock) -> ComputeService:
    d = compute_service_model_dict()
    item_id = COMPUTE_SERVICE_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return ComputeService(**d).save()


def identity_service_neomodel(db: MagicMock) -> IdentityService:
    d = identity_service_model_dict()
    item_id = IDENTITY_SERVICE_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return IdentityService(**d).save()


def network_service_neomodel(db: MagicMock) -> NetworkService:
    d = network_service_model_dict()
    item_id = NETWORK_SERVICE_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return NetworkService(**d).save()


def sla_neomodel(db: MagicMock) -> SLA:
    d = sla_model_dict()
    item_id = SLA_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return SLA(**d).save()


def user_group_neomodel(db: MagicMock) -> UserGroup:
    d = user_group_model_dict()
    item_id = USER_GROUP_ID + randint(0, 99)
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=item_id, properties=d)]],
        None,
    )
    return UserGroup(**d).save()


def connect_provider_and_idp_neomodel(
    db: MagicMock,
    *,
    provider: Provider,
    identity_provider: IdentityProvider,
):
    item_id = randint(0, 99)
    d = auth_method_dict()
    element_id = f"{db.database_version}:{uuid4().hex}:{item_id}"
    r = Relationship(..., element_id=element_id, id_=item_id, properties=d)
    r._start_node = Node(
        ...,
        element_id=provider.element_id,
        id_=int(provider.element_id[provider.element_id.rfind(":") + 1 :]),
    )
    r._end_node = Node(
        ...,
        element_id=identity_provider.element_id,
        id_=int(
            identity_provider.element_id[identity_provider.element_id.rfind(":") + 1 :]
        ),
    )
    db.cypher_query.return_value = ([[r]], None)
    return provider.identity_providers.connect(identity_provider, d)


def identity_provider_neomodel_query(n: int, db: MagicMock):
    items = []
    rels = None
    for _ in range(n):
        items.append(identity_provider_neomodel(db))
        rels = ["identity_providers_r1"]
    return [[i] for i in items], rels


def location_neomodel_query(n: int, db: MagicMock):
    items = []
    rels = None
    for _ in range(n):
        items.append(location_neomodel(db))
        rels = ["location_r1"]
    return [[i] for i in items], rels


def project_neomodel_query(n: int, db: MagicMock):
    items = []
    rels = None
    for _ in range(n):
        items.append(project_neomodel(db))
        rels = ["projects_r1"]
    return [[i] for i in items], rels


def provider_neomodel_query(n: int, db: MagicMock):
    items = []
    rels = None
    for _ in range(n):
        items.append(provider_neomodel(db))
        rels = ["providers_r1"]
    return [[i] for i in items], rels


def region_neomodel_query(n: int, db: MagicMock):
    items = []
    rels = None
    for _ in range(n):
        items.append(region_neomodel(db))
        rels = ["regions_r1"]
    return [[i] for i in items], rels


def block_storage_service_neomodel_query(n: int, db: MagicMock):
    items = []
    rels = None
    for _ in range(n):
        items.append(block_storage_service_neomodel(db))
        rels = ["block_storage_services_r1"]
    return [[i] for i in items], rels


def compute_service_neomodel_query(n: int, db: MagicMock):
    items = []
    rels = None
    for _ in range(n):
        items.append(compute_service_neomodel(db))
        rels = ["compute_services_r1"]
    return [[i] for i in items], rels


def identity_service_neomodel_query(n: int, db: MagicMock):
    items = []
    rels = None
    for _ in range(n):
        items.append(identity_service_neomodel(db))
        rels = ["identity_services_r1"]
    return [[i] for i in items], rels


def network_service_neomodel_query(n: int, db: MagicMock):
    items = []
    rels = None
    for _ in range(n):
        items.append(network_service_neomodel(db))
        rels = ["network_services_r1"]
    return [[i] for i in items], rels


def user_group_neomodel_query(n: int, db: MagicMock):
    items = []
    rels = None
    for _ in range(n):
        items.append(user_group_neomodel(db))
        rels = ["user_groups_r1"]
    return [[i] for i in items], rels
