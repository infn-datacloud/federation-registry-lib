from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.flavor.models import Flavor
from app.flavor.schemas import FlavorBase, FlavorUpdate
from app.provider.schemas_extended import FlavorCreateExtended
from tests.utils.api_v1 import BaseAPI
from tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)


class FlavorController(
    BaseAPI[Flavor, FlavorBase, FlavorBase, FlavorCreateExtended, FlavorUpdate]
):
    def _validate_create_relationships(
        self, *, obj: Dict[str, Any], db_item: Flavor, public: bool = False
    ) -> None:
        projects = obj.pop("projects")
        assert len(db_item.projects) == len(projects)
        for db_proj, proj_uuid in zip(
            sorted(db_item.projects, key=lambda x: x.uuid), sorted(projects)
        ):
            assert db_proj.uuid == proj_uuid
        return super()._validate_create_relationships(obj=obj, db_item=db_item)

    def _validate_read_relationships(
        self, *, obj: Dict[str, Any], db_item: Flavor, public: bool = False
    ) -> None:
        projects = obj.pop("projects")
        assert len(db_item.projects) == len(projects)
        for db_proj, proj_dict in zip(
            sorted(db_item.projects, key=lambda x: x.uid),
            sorted(projects, key=lambda x: x.get("uid")),
        ):
            assert db_proj.uid == proj_dict.get("uid")

        services = obj.pop("services")
        assert len(db_item.services) == len(services)
        for db_serv, serv_dict in zip(
            sorted(db_item.services, key=lambda x: x.uid),
            sorted(services, key=lambda x: x.get("uid")),
        ):
            assert db_serv.uid == serv_dict.get("uid")

        return super()._validate_read_relationships(
            obj=obj, db_item=db_item, public=public
        )

    def random_create_extended_item(
        self, *, default: bool = False, projects: Optional[List[str]] = None
    ) -> FlavorCreateExtended:
        if projects is None:
            projects = []
        name = random_lower_string()
        uuid = uuid4()
        kwargs = {}
        if not default:
            kwargs = {
                "description": random_lower_string(),
                "disk": random_non_negative_int(),
                "is_public": len(projects) == 0,
                "ram": random_non_negative_int(),
                "vcpus": random_non_negative_int(),
                "swap": random_non_negative_int(),
                "ephemeral": random_non_negative_int(),
                "infiniband_support": random_bool(),
                "gpus": random_positive_int(),
                "gpu_model": random_lower_string(),
                "gpu_vendor": random_lower_string(),
                "local_storage": random_lower_string(),
            }
            if len(projects) > 0:
                kwargs["projects"] = projects
        return super().random_create_extended_item(name=name, uuid=uuid, **kwargs)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[Flavor] = None, **kwargs
    ) -> FlavorUpdate:
        return super().random_patch_item(
            default=default,
            from_item=from_item,
            name=random_lower_string(),
            uuid=uuid4().hex,
            disk=random_non_negative_int(),
            ram=random_non_negative_int(),
            vcpus=random_non_negative_int(),
            swap=random_non_negative_int(),
            ephemeral=random_non_negative_int(),
            infiniband=random_bool(),
            gpus=random_positive_int(),
            gpu_model=random_lower_string(),
            gpu_vendor=random_lower_string(),
            local_storage=random_lower_string(),
            **kwargs,
        )
