from uuid import uuid4

import pytest
from app.image.models import Image
from app.image.schemas import ImageRead, ImageReadPublic, ImageReadShort
from app.image.schemas_extended import ImageReadExtended, ImageReadExtendedPublic
from pydantic import ValidationError
from tests.utils.image import (
    create_random_image,
    validate_read_extended_image_attrs,
    validate_read_extended_public_image_attrs,
    validate_read_image_attrs,
    validate_read_public_image_attrs,
    validate_read_short_image_attrs,
)


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_image()
    create_random_image(default=True)
    create_random_image(projects=[uuid4()])
    create_random_image(default=True, projects=[uuid4()])


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_image(projects=[uuid4()])
    with pytest.raises(ValidationError):
        a.uuid = None
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        # Empty projects list when the image is private
        assert not a.is_public
        a.projects = []
    with pytest.raises(ValidationError):
        # Public image with projects
        assert len(a.projects) > 0
        a.is_public = True
    with pytest.raises(ValidationError):
        # Duplicated projects
        a.projects = [a.projects[0], a.projects[0]]


def test_read_schema_public_image(db_public_image: Image):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target image is linked to a single service.
    """
    schema = ImageRead.from_orm(db_public_image)
    validate_read_image_attrs(obj_out=schema, db_item=db_public_image)
    schema = ImageReadShort.from_orm(db_public_image)
    validate_read_short_image_attrs(obj_out=schema, db_item=db_public_image)
    schema = ImageReadPublic.from_orm(db_public_image)
    validate_read_public_image_attrs(obj_out=schema, db_item=db_public_image)
    schema = ImageReadExtended.from_orm(db_public_image)
    validate_read_extended_image_attrs(obj_out=schema, db_item=db_public_image)
    schema = ImageReadExtendedPublic.from_orm(db_public_image)
    validate_read_extended_public_image_attrs(obj_out=schema, db_item=db_public_image)


def test_read_schema_private_image_single_project(db_private_image: Image):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target image is linked to a single service and owned by a single
    project.
    """
    schema = ImageRead.from_orm(db_private_image)
    validate_read_image_attrs(obj_out=schema, db_item=db_private_image)
    schema = ImageReadShort.from_orm(db_private_image)
    validate_read_short_image_attrs(obj_out=schema, db_item=db_private_image)
    schema = ImageReadPublic.from_orm(db_private_image)
    validate_read_public_image_attrs(obj_out=schema, db_item=db_private_image)
    schema = ImageReadExtended.from_orm(db_private_image)
    validate_read_extended_image_attrs(obj_out=schema, db_item=db_private_image)
    schema = ImageReadExtendedPublic.from_orm(db_private_image)
    validate_read_extended_public_image_attrs(
        obj_out=schema, db_item=db_private_image
    )


def test_read_schema_private_image_multiple_projects(
    db_private_image_multiple_projects: Image,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target image is linked to a single service and owned by multiple
    projects on the same provider.
    """
    schema = ImageRead.from_orm(db_private_image_multiple_projects)
    validate_read_image_attrs(
        obj_out=schema, db_item=db_private_image_multiple_projects
    )
    schema = ImageReadShort.from_orm(db_private_image_multiple_projects)
    validate_read_short_image_attrs(
        obj_out=schema, db_item=db_private_image_multiple_projects
    )
    schema = ImageReadPublic.from_orm(db_private_image_multiple_projects)
    validate_read_public_image_attrs(
        obj_out=schema, db_item=db_private_image_multiple_projects
    )
    schema = ImageReadExtended.from_orm(db_private_image_multiple_projects)
    validate_read_extended_image_attrs(
        obj_out=schema, db_item=db_private_image_multiple_projects
    )
    schema = ImageReadExtendedPublic.from_orm(db_private_image_multiple_projects)
    validate_read_extended_public_image_attrs(
        obj_out=schema, db_item=db_private_image_multiple_projects
    )


# TODO Add tests for a image shared between multiple services
