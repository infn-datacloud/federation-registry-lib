"""Module to test Schemas creation, patch and read."""
import pytest
from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from tests.flavor.cases_schemas import (
    InvalidCreateData,
    InvalidPatchData,
    ReadSchemaProperties,
    ValidCreateData,
    ValidPatchData,
)


class TestSchemaCreation:
    """Test create schemas."""

    @parametrize_with_cases("cls, validator, data", cases=ValidCreateData)
    def test_create_schema(self, cls, validator, data) -> None:
        """Create a schema from a dict."""
        schema = cls(**data)
        validator.validate_create_ext_attrs(data=data, schema=schema)

    @parametrize_with_cases("cls, data", cases=InvalidCreateData)
    def test_create_invalid_schema(self, cls, data) -> None:
        """The schema creation fails and raises an error."""
        with pytest.raises(ValidationError):
            cls(**data)


class TestSchemaPatch:
    """Test patch schemas."""

    @parametrize_with_cases("cls, validator, data", cases=ValidPatchData)
    def test_create_schema(self, cls, validator, data) -> None:
        """Create a schema from a dict."""
        schema = cls(**data)
        validator.validate_attrs(data=data, schema=schema)

    @parametrize_with_cases("cls, data", cases=InvalidPatchData)
    def test_create_invalid_schema(self, cls, data) -> None:
        """The schema creation fails and raises an error."""
        with pytest.raises(ValidationError):
            cls(**data)


class TestSchemaRead:
    """Test read schemas."""

    @parametrize_with_cases(
        "cls, validator, public, extended, db_item", cases=ReadSchemaProperties
    )
    def test_db_item(self, cls, validator, public, extended, db_item) -> None:
        """Create a schema from a dict."""
        schema = cls.from_orm(db_item)
        validator.validate_read_attrs(
            db_item=db_item, schema=schema, public=public, extended=extended
        )
