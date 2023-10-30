import pytest
from app.project.models import Project
from app.project.schemas import ProjectRead, ProjectReadPublic, ProjectReadShort
from app.project.schemas_extended import ProjectReadExtended, ProjectReadExtendedPublic
from pydantic import ValidationError
from tests.utils.project import (
    create_random_project,
    validate_read_extended_project_attrs,
    validate_read_extended_public_project_attrs,
    validate_read_project_attrs,
    validate_read_public_project_attrs,
    validate_read_short_project_attrs,
)


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_project()
    create_random_project(default=True)


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_project()
    with pytest.raises(ValidationError):
        a.uuid = None
    with pytest.raises(ValidationError):
        a.name = None


def test_read_schema(db_project: Project):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target project has no relationships except for provider.
    """
    schema = ProjectRead.from_orm(db_project)
    validate_read_project_attrs(obj_out=schema, db_item=db_project)
    schema = ProjectReadShort.from_orm(db_project)
    validate_read_short_project_attrs(obj_out=schema, db_item=db_project)
    schema = ProjectReadPublic.from_orm(db_project)
    validate_read_public_project_attrs(obj_out=schema, db_item=db_project)
    schema = ProjectReadExtended.from_orm(db_project)
    validate_read_extended_project_attrs(obj_out=schema, db_item=db_project)
    schema = ProjectReadExtendedPublic.from_orm(db_project)
    validate_read_extended_public_project_attrs(obj_out=schema, db_item=db_project)


def test_read_schema_with_single_block_storage_quota(
    db_project_with_single_block_storage_quota: Project,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target project has no relationships except for provider.
    """
    schema = ProjectRead.from_orm(db_project_with_single_block_storage_quota)
    validate_read_project_attrs(
        obj_out=schema, db_item=db_project_with_single_block_storage_quota
    )
    schema = ProjectReadShort.from_orm(db_project_with_single_block_storage_quota)
    validate_read_short_project_attrs(
        obj_out=schema, db_item=db_project_with_single_block_storage_quota
    )
    schema = ProjectReadPublic.from_orm(db_project_with_single_block_storage_quota)
    validate_read_public_project_attrs(
        obj_out=schema, db_item=db_project_with_single_block_storage_quota
    )
    schema = ProjectReadExtended.from_orm(db_project_with_single_block_storage_quota)
    validate_read_extended_project_attrs(
        obj_out=schema, db_item=db_project_with_single_block_storage_quota
    )
    schema = ProjectReadExtendedPublic.from_orm(
        db_project_with_single_block_storage_quota
    )
    validate_read_extended_public_project_attrs(
        obj_out=schema, db_item=db_project_with_single_block_storage_quota
    )


def test_read_schema_with_multiple_block_storage_quotas(
    db_project_with_multiple_block_storage_quotas_diff_service: Project,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target project has no relationships except for provider.
    """
    schema = ProjectRead.from_orm(
        db_project_with_multiple_block_storage_quotas_diff_service
    )
    validate_read_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_block_storage_quotas_diff_service,
    )
    schema = ProjectReadShort.from_orm(
        db_project_with_multiple_block_storage_quotas_diff_service
    )
    validate_read_short_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_block_storage_quotas_diff_service,
    )
    schema = ProjectReadPublic.from_orm(
        db_project_with_multiple_block_storage_quotas_diff_service
    )
    validate_read_public_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_block_storage_quotas_diff_service,
    )
    schema = ProjectReadExtended.from_orm(
        db_project_with_multiple_block_storage_quotas_diff_service
    )
    assert len(schema.quotas) > 1
    validate_read_extended_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_block_storage_quotas_diff_service,
    )
    schema = ProjectReadExtendedPublic.from_orm(
        db_project_with_multiple_block_storage_quotas_diff_service
    )
    assert len(schema.quotas) > 1
    validate_read_extended_public_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_block_storage_quotas_diff_service,
    )


def test_read_schema_with_single_compute_quota(
    db_project_with_single_compute_quota: Project,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target project has a provider and a compute quota.
    """
    schema = ProjectRead.from_orm(db_project_with_single_compute_quota)
    validate_read_project_attrs(
        obj_out=schema, db_item=db_project_with_single_compute_quota
    )
    schema = ProjectReadShort.from_orm(db_project_with_single_compute_quota)
    validate_read_short_project_attrs(
        obj_out=schema, db_item=db_project_with_single_compute_quota
    )
    schema = ProjectReadPublic.from_orm(db_project_with_single_compute_quota)
    validate_read_public_project_attrs(
        obj_out=schema, db_item=db_project_with_single_compute_quota
    )
    schema = ProjectReadExtended.from_orm(db_project_with_single_compute_quota)
    validate_read_extended_project_attrs(
        obj_out=schema, db_item=db_project_with_single_compute_quota
    )
    schema = ProjectReadExtendedPublic.from_orm(db_project_with_single_compute_quota)
    validate_read_extended_public_project_attrs(
        obj_out=schema, db_item=db_project_with_single_compute_quota
    )


def test_read_schema_with_multiple_compute_quotas(
    db_project_with_multiple_compute_quotas_diff_service: Project,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target project has a provider and multiple compute quotas.
    """
    schema = ProjectRead.from_orm(db_project_with_multiple_compute_quotas_diff_service)
    validate_read_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_compute_quotas_diff_service,
    )
    schema = ProjectReadShort.from_orm(
        db_project_with_multiple_compute_quotas_diff_service
    )
    validate_read_short_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_compute_quotas_diff_service,
    )
    schema = ProjectReadPublic.from_orm(
        db_project_with_multiple_compute_quotas_diff_service
    )
    validate_read_public_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_compute_quotas_diff_service,
    )
    schema = ProjectReadExtended.from_orm(
        db_project_with_multiple_compute_quotas_diff_service
    )
    assert len(schema.quotas) > 1
    validate_read_extended_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_compute_quotas_diff_service,
    )
    schema = ProjectReadExtendedPublic.from_orm(
        db_project_with_multiple_compute_quotas_diff_service
    )
    assert len(schema.quotas) > 1
    validate_read_extended_public_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_compute_quotas_diff_service,
    )


def test_read_schema_with_single_flavor(
    db_project_with_single_private_flavor: Project,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target project has a provider and a flavor.
    """
    schema = ProjectRead.from_orm(db_project_with_single_private_flavor)
    validate_read_project_attrs(
        obj_out=schema, db_item=db_project_with_single_private_flavor
    )
    schema = ProjectReadShort.from_orm(db_project_with_single_private_flavor)
    validate_read_short_project_attrs(
        obj_out=schema, db_item=db_project_with_single_private_flavor
    )
    schema = ProjectReadPublic.from_orm(db_project_with_single_private_flavor)
    validate_read_public_project_attrs(
        obj_out=schema, db_item=db_project_with_single_private_flavor
    )
    schema = ProjectReadExtended.from_orm(db_project_with_single_private_flavor)
    validate_read_extended_project_attrs(
        obj_out=schema, db_item=db_project_with_single_private_flavor
    )
    schema = ProjectReadExtendedPublic.from_orm(db_project_with_single_private_flavor)
    validate_read_extended_public_project_attrs(
        obj_out=schema, db_item=db_project_with_single_private_flavor
    )


def test_read_schema_with_multiple_flavors(
    db_project_with_multiple_private_flavors_diff_service: Project,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target project has a provider and multiple flavors.
    """
    schema = ProjectRead.from_orm(db_project_with_multiple_private_flavors_diff_service)
    validate_read_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_private_flavors_diff_service,
    )
    schema = ProjectReadShort.from_orm(
        db_project_with_multiple_private_flavors_diff_service
    )
    validate_read_short_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_private_flavors_diff_service,
    )
    schema = ProjectReadPublic.from_orm(
        db_project_with_multiple_private_flavors_diff_service
    )
    validate_read_public_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_private_flavors_diff_service,
    )
    schema = ProjectReadExtended.from_orm(
        db_project_with_multiple_private_flavors_diff_service
    )
    assert len(schema.private_flavors) > 1
    validate_read_extended_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_private_flavors_diff_service,
    )
    schema = ProjectReadExtendedPublic.from_orm(
        db_project_with_multiple_private_flavors_diff_service
    )
    assert len(schema.private_flavors) > 1
    validate_read_extended_public_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_private_flavors_diff_service,
    )


def test_read_schema_with_single_image(
    db_project_with_single_private_image: Project,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target project has a provider and an image.
    """
    schema = ProjectRead.from_orm(db_project_with_single_private_image)
    validate_read_project_attrs(
        obj_out=schema, db_item=db_project_with_single_private_image
    )
    schema = ProjectReadShort.from_orm(db_project_with_single_private_image)
    validate_read_short_project_attrs(
        obj_out=schema, db_item=db_project_with_single_private_image
    )
    schema = ProjectReadPublic.from_orm(db_project_with_single_private_image)
    validate_read_public_project_attrs(
        obj_out=schema, db_item=db_project_with_single_private_image
    )
    schema = ProjectReadExtended.from_orm(db_project_with_single_private_image)
    validate_read_extended_project_attrs(
        obj_out=schema, db_item=db_project_with_single_private_image
    )
    schema = ProjectReadExtendedPublic.from_orm(db_project_with_single_private_image)
    validate_read_extended_public_project_attrs(
        obj_out=schema, db_item=db_project_with_single_private_image
    )


def test_read_schema_with_multiple_images(
    db_project_with_multiple_private_images_diff_service: Project,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target project has a provider and multiple images.
    """
    schema = ProjectRead.from_orm(db_project_with_multiple_private_images_diff_service)
    validate_read_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_private_images_diff_service,
    )
    schema = ProjectReadShort.from_orm(
        db_project_with_multiple_private_images_diff_service
    )
    validate_read_short_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_private_images_diff_service,
    )
    schema = ProjectReadPublic.from_orm(
        db_project_with_multiple_private_images_diff_service
    )
    validate_read_public_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_private_images_diff_service,
    )
    schema = ProjectReadExtended.from_orm(
        db_project_with_multiple_private_images_diff_service
    )
    assert len(schema.private_images) > 1
    validate_read_extended_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_private_images_diff_service,
    )
    schema = ProjectReadExtendedPublic.from_orm(
        db_project_with_multiple_private_images_diff_service
    )
    assert len(schema.private_images) > 1
    validate_read_extended_public_project_attrs(
        obj_out=schema,
        db_item=db_project_with_multiple_private_images_diff_service,
    )
