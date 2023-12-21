"""Module to test Schemas creation, patch and read."""
import pytest
from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

CASES = [
    "tests.flavor.cases_schemas",
    "tests.identity_provider.cases_schemas",
    "tests.image.cases_schemas",
    "tests.location.cases_schemas",
    "tests.network.cases_schemas",
    "tests.project.cases_schemas",
    "tests.provider.cases_schemas",
    "tests.quotas.block_storage_quota.cases_schemas",
    "tests.quotas.compute_quota.cases_schemas",
    "tests.quotas.network_quota.cases_schemas",
    "tests.region.cases_schemas",
    "tests.services.block_storage_service.cases_schemas",
    "tests.services.compute_service.cases_schemas",
    "tests.services.identity_service.cases_schemas",
    "tests.services.network_service.cases_schemas",
    "tests.sla.cases_schemas",
    "tests.user_group.cases_schemas",
]


class TestSchema:
    """Test create, patch and read schemas."""

    @parametrize_with_cases("cls, validator, data", cases=CASES, has_tag="create_valid")
    def test_create_valid_schema(self, cls, validator, data) -> None:
        """Create a schema from a dict."""
        schema = cls(**data)
        validator.validate_create_ext_attrs(data=data, schema=schema)

    @parametrize_with_cases("cls, data", cases=CASES, has_tag="create_invalid")
    def test_create_invalid_schema(self, cls, data) -> None:
        """The schema creation fails and raises an error."""
        with pytest.raises(ValidationError):
            cls(**data)

    @parametrize_with_cases("cls, validator, data", cases=CASES, has_tag="patch_valid")
    def test_patch_valid_schema(self, cls, validator, data) -> None:
        """Create a schema from a dict."""
        schema = cls(**data)
        validator.validate_attrs(data=data, schema=schema)

    @parametrize_with_cases("cls, data", cases=CASES, has_tag="patch_invalid")
    def test_patch_invalid_schema(self, cls, data) -> None:
        """The schema creation fails and raises an error."""
        with pytest.raises(ValidationError):
            cls(**data)

    @parametrize_with_cases(
        "cls, validator, db_item, public, extended", cases=CASES, has_tag="read"
    )
    def test_read_schema(self, cls, validator, db_item, public, extended) -> None:
        """Create a schema from a dict."""
        schema = cls.from_orm(db_item)
        validator.validate_read_attrs(
            db_item=db_item, schema=schema, public=public, extended=extended
        )
