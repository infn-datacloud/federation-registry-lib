"""Module to test Flavor schema creation."""
from typing import Any, Dict

import pytest
from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from app.flavor.schemas import FlavorUpdate
from tests.flavor.schema import BaseSchemaValidation, InvalidPatchData, ValidPatchData


class TestFlavorSchemaPatch(BaseSchemaValidation):
    """Test flavor schemas."""

    @parametrize_with_cases("data", cases=ValidPatchData)
    def test_create_schema(self, data: Dict[str, Any]) -> None:
        """Create a schema from a dict."""
        schema = FlavorUpdate(**data)
        self.validate_attrs(data=data, schema=schema)

    @parametrize_with_cases("data", cases=InvalidPatchData)
    def test_create_invalid_schema(self, data) -> None:
        """The schema creation fails and raises an error."""
        with pytest.raises(ValidationError):
            FlavorUpdate(**data)
