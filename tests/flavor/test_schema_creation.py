"""Module to test Flavor schema creation."""
import pytest
from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from app.provider.schemas_extended import FlavorCreateExtended
from tests.flavor.cases_schemas import InvalidCreateData, ValidCreateData
from tests.flavor.schema import (
    CreateSchemaValidation,
)


class TestFlavorSchemaCreation(CreateSchemaValidation):
    """Test flavor schemas."""

    @parametrize_with_cases("data", cases=ValidCreateData)
    def test_create_schema(self, data) -> None:
        """Create a schema from a dict."""
        schema = FlavorCreateExtended(**data)
        self.validate_create_ext_attrs(data=data, schema=schema)

    @parametrize_with_cases("data", cases=InvalidCreateData)
    def test_create_invalid_schema(self, data) -> None:
        """The schema creation fails and raises an error."""
        with pytest.raises(ValidationError):
            FlavorCreateExtended(**data)
