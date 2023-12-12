"""Module to test Schemas creation, patch and read."""
import pytest
from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from tests.flavor.cases_schemas import SchemaCases


class TestSchema:
    """Test create, patch and read schemas."""

    @parametrize_with_cases(
        "cls, validator, data", cases=SchemaCases, has_tag="create_valid"
    )
    def test_create_valid_schema(self, cls, validator, data) -> None:
        """Create a schema from a dict."""
        schema = cls(**data)
        validator.validate_create_ext_attrs(data=data, schema=schema)

    @parametrize_with_cases("cls, data", cases=SchemaCases, has_tag="create_invalid")
    def test_create_invalid_schema(self, cls, data) -> None:
        """The schema creation fails and raises an error."""
        with pytest.raises(ValidationError):
            cls(**data)

    @parametrize_with_cases(
        "cls, validator, data", cases=SchemaCases, has_tag="patch_valid"
    )
    def test_patch_valid_schema(self, cls, validator, data) -> None:
        """Create a schema from a dict."""
        schema = cls(**data)
        validator.validate_attrs(data=data, schema=schema)

    @parametrize_with_cases("cls, data", cases=SchemaCases, has_tag="patch_invalid")
    def test_patch_invalid_schema(self, cls, data) -> None:
        """The schema creation fails and raises an error."""
        with pytest.raises(ValidationError):
            cls(**data)

    @parametrize_with_cases(
        "cls, validator, public, extended, db_item", cases=SchemaCases, has_tag="read"
    )
    def test_read_schema(self, cls, validator, public, extended, db_item) -> None:
        """Create a schema from a dict."""
        schema = cls.from_orm(db_item)
        validator.validate_read_attrs(
            db_item=db_item, schema=schema, public=public, extended=extended
        )
