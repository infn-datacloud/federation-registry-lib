from uuid import uuid4

import pytest
from app.image.crud import image
from app.image.schemas import ImageRead, ImageReadPublic, ImageReadShort
from app.image.schemas_extended import ImageReadExtended, ImageReadExtendedPublic
from app.service.models import ComputeService
from pydantic import ValidationError
from tests.utils.image import create_random_image


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


def test_read_schema(db_compute_serv: ComputeService):
    """Create a valid 'Read' Schema."""
    obj_in = create_random_image()
    db_obj = image.create(obj_in=obj_in, service=db_compute_serv)
    ImageRead.from_orm(db_obj)
    ImageReadPublic.from_orm(db_obj)
    ImageReadShort.from_orm(db_obj)
    ImageReadExtended.from_orm(db_obj)
    ImageReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_image(default=True)
    db_obj = image.create(obj_in=obj_in, service=db_compute_serv)
    ImageRead.from_orm(db_obj)
    ImageReadPublic.from_orm(db_obj)
    ImageReadShort.from_orm(db_obj)
    ImageReadExtended.from_orm(db_obj)
    ImageReadExtendedPublic.from_orm(db_obj)

    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    obj_in = create_random_image(projects=[i.uuid for i in db_provider.projects])
    db_obj = image.create(obj_in=obj_in, service=db_compute_serv)
    ImageRead.from_orm(db_obj)
    ImageReadPublic.from_orm(db_obj)
    ImageReadShort.from_orm(db_obj)
    ImageReadExtended.from_orm(db_obj)
    ImageReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_image(
        default=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = image.create(obj_in=obj_in, service=db_compute_serv)
    ImageRead.from_orm(db_obj)
    ImageReadPublic.from_orm(db_obj)
    ImageReadShort.from_orm(db_obj)
    ImageReadExtended.from_orm(db_obj)
    ImageReadExtendedPublic.from_orm(db_obj)
