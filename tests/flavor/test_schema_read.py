"""Module to test Flavor schema creation."""
from pytest_cases import fixture_ref, parametrize, parametrize_with_cases

from app.flavor.models import Flavor
from app.flavor.schemas import FlavorRead, FlavorReadPublic
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from tests.flavor.cases_schemas import ReadSchemaConnection, ReadSchemaVisibility
from tests.flavor.schema import ReadSchemaValidation


class TestFlavorSchemaRead(ReadSchemaValidation):
    """Test flavor schemas."""

    @parametrize("db_item", {fixture_ref("db_flavor"), fixture_ref("db_shared_flavor")})
    @parametrize_with_cases("public", cases=ReadSchemaVisibility)
    @parametrize_with_cases("extended", cases=ReadSchemaConnection)
    def test_db_item(self, public: bool, extended: bool, db_item: Flavor) -> None:
        """Create a schema from a dict."""
        if public and not extended:
            schema = FlavorReadPublic.from_orm(db_item)
        elif public and extended:
            schema = FlavorReadExtendedPublic.from_orm(db_item)
        elif not public and not extended:
            schema = FlavorRead.from_orm(db_item)
        else:
            schema = FlavorReadExtended.from_orm(db_item)
        self.validate_read_attrs(
            db_item=db_item, schema=schema, public=public, extended=extended
        )
