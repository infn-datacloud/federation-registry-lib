from typing import Any, Literal

from pytest_cases import case, parametrize_with_cases

from fedreg.v1.region.models import Region
from fedreg.v1.region.schemas import RegionBase, RegionCreate
from tests.v1.schemas.utils import region_schema_dict
from tests.v1.utils import random_lower_string


class CaseRegionSchema:
    @case(tags=("dict", "valid", "base_public", "base", "update"))
    def case_mandatory(self) -> dict[str, Any]:
        return region_schema_dict()

    @case(tags=("dict", "valid", "base_public", "base", "update"))
    def case_description(self) -> dict[str, Any]:
        return {**region_schema_dict(), "description": random_lower_string()}

    @case(tags=("dict", "invalid", "base_public", "base", "read_public", "read"))
    def case_missing_name(self) -> tuple[dict[str, Any], Literal["name"]]:
        d = region_schema_dict()
        d.pop("name")
        return d, "name"

    @case(tags="class")
    def case_base_class(self) -> type[RegionBase]:
        return RegionBase

    @case(tags="class")
    def case_create_class(self) -> type[RegionCreate]:
        return RegionCreate


class CaseRegionModel:
    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseRegionSchema, has_tag=("dict", "valid", "base")
    )
    def case_region_model(self, data: dict[str, Any]) -> Region:
        return Region(**RegionBase(**data).dict()).save()
