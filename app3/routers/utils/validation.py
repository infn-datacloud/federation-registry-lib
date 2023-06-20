from fastapi import HTTPException, status
from pydantic import UUID4, BaseModel
from typing import Callable, List, Mapping

from ... import crud


class CheckItemExist:
    def __init__(self, class_name: str, get_item: Callable):
        self.class_name = class_name
        self.get_item = get_item

    def __call__(self, uid: UUID4) -> Mapping:
        item = self.get_item(uid=str(uid).replace("-", ""))
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.class_name} {uid} not found",
            )
        return item


class CheckItemUnique:
    def __init__(
        self, class_name: str, get_item: Callable, attribute_names: List[str]
    ):
        self.class_name = class_name
        self.get_item = get_item
        self.attribute_names = attribute_names

    def __call__(self, item: BaseModel) -> Mapping:
        d = item.dict()
        kwargs = {}
        for k in self.attribute_names:
            kwargs[k] = d.get(k)
        item = self.get_item(**kwargs)
        if item:
            props = []
            for k, v in kwargs.items():
                props.append(f"{k} = {v}")
            props = ",".join(props)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{self.class_name} with {props} already exists",
            )
        return item


valid_cluster_id = CheckItemExist("Cluster", crud.cluster.read_cluster)
valid_flavor_id = CheckItemExist("Flavor", crud.flavor.read_flavor)
valid_identity_provider_id = CheckItemExist(
    "IdentityProvider", crud.identity_provider.read_identity_provider
)
valid_image_id = CheckItemExist("Image", crud.image.read_image)
valid_location_id = CheckItemExist("Location", crud.location.read_location)
valid_project_id = CheckItemExist("Project", crud.project.read_project)
valid_provider_id = CheckItemExist("Provider", crud.provider.read_provider)
valid_quota_id = CheckItemExist("Quota", crud.quota.read_quota)
valid_quota_type_id = CheckItemExist(
    "QuotaType", crud.quota_type.read_quota_type
)
valid_service_id = CheckItemExist("Service", crud.service.read_service)
valid_service_type_id = CheckItemExist(
    "serviceType", crud.service_type.read_service_type
)
valid_sla_id = CheckItemExist("SLA", crud.sla.read_sla)
valid_user_group_id = CheckItemExist(
    "UserGroup", crud.user_group.read_user_group
)

# is_unique_cluster_id = CheckItemUnique("Cluster", crud.cluster.read_cluster)
# is_unique_flavor_id = CheckItemUnique("Flavor", crud.flavor.read_flavor)
# is_unique_identity_provider_id = CheckItemUnique(
#     "IdentityProvider",
#     crud.identity_provider.read_identity_provider,
#     ["endpoint"],
# )
# is_unique_image_id = CheckItemUnique("Image", crud.image.read_image)
# is_unique_location_id = CheckItemUnique(
#     "Location", crud.location.read_location
# )
# is_unique_project_id = CheckItemUnique("Project", crud.project.read_project)
# is_unique_provider_id = CheckItemUnique(
#     "Provider", crud.provider.read_provider
# )
# is_unique_quota_id = CheckItemUnique("Quota", crud.quota.read_quota)
# is_unique_quota_type_id = CheckItemUnique(
#     "QuotaType", crud.quota_type.read_quota_type
# )
# is_unique_service_id = CheckItemUnique("Service", crud.service.read_service)
# is_unique_service_type_id = CheckItemUnique(
#     "serviceType", crud.service_type.read_service_type
# )
# is_unique_sla_id = CheckItemUnique("SLA", crud.sla.read_sla)
# is_unique_user_group_id = CheckItemUnique(
#     "UserGroup", crud.user_group.read_user_group
# )
#
