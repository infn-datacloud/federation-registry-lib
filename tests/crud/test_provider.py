from typing import Generator
from uuid import uuid4

from app.identity_provider.crud import identity_provider
from app.project.crud import project
from app.provider.crud import provider
from app.provider.models import Provider
from app.region.crud import region
from tests.utils.provider import (
    create_random_provider,
    create_random_provider_patch,
    validate_create_provider_attrs,
)


def test_create_item(setup_and_teardown_db: Generator) -> None:
    """Create a Provider."""
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    """Create a Provider, with default values when possible."""
    item_in = create_random_provider(default=True)
    item = provider.create(obj_in=item_in)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects(setup_and_teardown_db: Generator) -> None:
    """Create a Provider, with linked projects."""
    item_in = create_random_provider(with_projects=True)
    item = provider.create(obj_in=item_in)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects_and_identity_providers(
    setup_and_teardown_db: Generator,
) -> None:
    """Create a Provider, with linked projects and identity providers."""
    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item = provider.create(obj_in=item_in)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects_and_regions(
    setup_and_teardown_db: Generator,
) -> None:
    """Create a Provider, with linked projects and regions."""
    item_in = create_random_provider(with_projects=True, with_regions=True)
    item = provider.create(obj_in=item_in)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_regions(
    setup_and_teardown_db: Generator,
) -> None:
    """Create a Provider, with regions and no projects."""
    item_in = create_random_provider(with_regions=True)
    item = provider.create(obj_in=item_in)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_everything(setup_and_teardown_db: Generator) -> None:
    """Create a Provider, with linked projects, identity providers and regions."""
    item_in = create_random_provider(
        with_projects=True, with_identity_providers=True, with_regions=True
    )
    item = provider.create(obj_in=item_in)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_provider: Provider) -> None:
    """Retrieve a Provider from its UID."""
    item = provider.get(uid=db_provider.uid)
    assert item.uid == db_provider.uid


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
    """Try to retrieve a not existing Provider."""
    assert not provider.get(uid=uuid4())


def test_get_items(db_provider: Provider, db_provider2: Provider) -> None:
    """Retrieve multiple Providers."""
    stored_items = provider.get_multi()
    assert len(stored_items) == 2

    stored_items = provider.get_multi(uid=db_provider.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_provider.uid

    stored_items = provider.get_multi(uid=db_provider2.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_provider2.uid


def test_get_items_with_limit(db_provider: Provider, db_provider2: Provider) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = provider.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = provider.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = provider.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_provider: Provider, db_provider2: Provider) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = sorted(provider.get_multi(), key=lambda x: x.uid)

    stored_items = provider.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = provider.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_provider: Provider, db_provider2: Provider) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = provider.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = provider.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_provider: Provider) -> None:
    """Update the attributes of an existing Provider, without updating its
    relationships.
    """
    patch_in = create_random_provider_patch()
    item = provider.update(db_obj=db_provider, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_provider: Provider) -> None:
    """Try to update the attributes of an existing Provider, without updating its
    relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit default values,
    succeeds.
    """
    patch_in = create_random_provider_patch(default=True)
    assert not provider.update(db_obj=db_provider, obj_in=patch_in)

    patch_in = create_random_provider_patch(default=True)
    patch_in.description = ""
    item = provider.update(db_obj=db_provider, obj_in=patch_in)
    assert item.description == patch_in.description
    for k, v in db_provider.__dict__.items():
        if k != "description":
            assert item.__getattribute__(k) == v


def test_add_project(db_provider: Provider) -> None:
    """Update the attributes and relationships of an existing Provider.

    Update a Provider with no projects, changing its attributes and linking new
    projects.
    """
    item_in = create_random_provider(with_projects=True)
    item = provider.update(db_obj=db_provider, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.projects) > 0


def test_remove_project(db_provider_with_single_project: Provider) -> None:
    """Update the attributes and relationships of an existing Provider.

    At first update a Provider with a set of projects, updating its attributes and
    removing the existing projects.
    """
    item_in = create_random_provider()
    item = provider.update(
        db_obj=db_provider_with_single_project, obj_in=item_in, force=True
    )
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.projects) == 0


def test_replace_projects(db_provider_with_single_project: Provider) -> None:
    """Update the attributes and relationships of an existing Provider.

    Update a Provider with a set of projects, changing both its attributes and replacing
    the existing projects with new ones.
    """
    db_project = db_provider_with_single_project.projects.single()
    item_in = create_random_provider(with_projects=True)
    item = provider.update(
        db_obj=db_provider_with_single_project, obj_in=item_in, force=True
    )
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.projects) == 1
    assert item.projects.single() != db_project


def test_force_update_without_changing_projects(
    db_provider_with_single_project: Provider,
) -> None:
    """Update the attributes and relationships of an existing Provider.

    Update a Provider with a set of projects, changing only its attributes leaving
    untouched its connections (this is different from the previous test because the flag
    force is set to True).
    """
    db_project = db_provider_with_single_project.projects.single()
    item_in = create_random_provider(with_projects=True)
    item_in.projects[0].uuid = db_project.uuid
    item_in.projects[0].name = db_project.name
    item = provider.update(
        db_obj=db_provider_with_single_project, obj_in=item_in, force=True
    )
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.projects) == 1
    assert item.projects.single() == db_project


def test_add_identity_provider(db_provider: Provider) -> None:
    """Update the attributes and relationships of an existing Provider.

    Update a Provider with no identity_providers, changing its attributes and linking
    new identity_providers.
    """
    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item = provider.update(db_obj=db_provider, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.identity_providers) > 0


def test_remove_identity_provider(db_provider_with_single_idp: Provider) -> None:
    """Update the attributes and relationships of an existing Provider.

    At first update a Provider with a set of identity_providers, updating its attributes
    and removing the existing identity_providers.
    """
    item_in = create_random_provider()
    item = provider.update(
        db_obj=db_provider_with_single_idp, obj_in=item_in, force=True
    )
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.identity_providers) == 0


def test_remove_shared_identity_provider(db_provider_with_shared_idp: Provider) -> None:
    """Update the attributes and relationships of an existing identity provider.

    Update an identity provider with a set of linked identity_provider, updating its
    attributes and removing all linked identity_provider.
    """
    db_identity_provider = db_provider_with_shared_idp.identity_providers.single()
    item_in = create_random_provider()
    item = provider.update(
        db_obj=db_provider_with_shared_idp, obj_in=item_in, force=True
    )
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.identity_providers) == 0
    assert identity_provider.get(uid=db_identity_provider.uid)


def test_replace_identity_providers(
    db_provider_with_single_idp: Provider,
) -> None:
    """Update the attributes and relationships of an existing Provider.

    Update a Provider with a set of identity_providers, changing both its attributes and
    replacing the existing identity_providers with new ones.
    """
    db_identity_provider = db_provider_with_single_idp.identity_providers.single()
    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item = provider.update(
        db_obj=db_provider_with_single_idp, obj_in=item_in, force=True
    )
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.identity_providers) == 1
    assert item.identity_providers.single() != db_identity_provider


def test_force_update_without_changing_identity_providers(
    db_provider_with_single_idp: Provider,
) -> None:
    """Update the attributes and relationships of an existing Provider.

    Update a Provider with a set of identity_providers, changing only its attributes
    leaving untouched its connections (this is different from the previous test because
    the flag force is set to True).
    """
    db_identity_provider = db_provider_with_single_idp.identity_providers.single()
    rel = db_provider_with_single_idp.identity_providers.relationship(
        db_identity_provider
    )
    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item_in.identity_providers[0].endpoint = db_identity_provider.endpoint
    item_in.identity_providers[0].group_claim = db_identity_provider.group_claim
    item_in.identity_providers[0].relationship.idp_name = rel.idp_name
    item_in.identity_providers[0].relationship.protocol = rel.protocol
    item = provider.update(
        db_obj=db_provider_with_single_idp, obj_in=item_in, force=True
    )
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.identity_providers) == 1
    assert item.identity_providers.single() == db_identity_provider
    db_rel = item.identity_providers.relationship(db_identity_provider)
    assert db_rel.idp_name == rel.idp_name
    assert db_rel.protocol == rel.protocol


def test_add_region(db_provider: Provider) -> None:
    """Update the attributes and relationships of an existing Provider.

    Update a Provider with no regions, changing its attributes and linking new regions.
    """
    item_in = create_random_provider(with_regions=True)
    item = provider.update(db_obj=db_provider, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.regions) > 0


def test_remove_region(db_provider_with_single_region: Provider) -> None:
    """Update the attributes and relationships of an existing Provider.

    At first update a Provider with a set of regions, updating its attributes and
    removing the existing regions.
    """
    item_in = create_random_provider()
    item = provider.update(
        db_obj=db_provider_with_single_region, obj_in=item_in, force=True
    )
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.regions) == 0


def test_replace_regions(db_provider_with_single_region: Provider) -> None:
    """Update the attributes and relationships of an existing Provider.

    Update a Provider with a set of regions, changing both its attributes and replacing
    the existing regions with new ones.
    """
    db_region = db_provider_with_single_region.regions.single()
    item_in = create_random_provider(with_regions=True)
    item = provider.update(
        db_obj=db_provider_with_single_region, obj_in=item_in, force=True
    )
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.regions) == 1
    assert item.regions.single() != db_region


def test_force_update_without_changing_regions(
    db_provider_with_single_region: Provider,
) -> None:
    """Update the attributes and relationships of an existing Provider.

    Update a Provider with a set of regions, changing only its attributes leaving
    untouched its connections (this is different from the previous test because the flag
    force is set to True).
    """
    db_region = db_provider_with_single_region.regions.single()
    item_in = create_random_provider(with_regions=True)
    item_in.regions[0].name = db_region.name
    item = provider.update(
        db_obj=db_provider_with_single_region, obj_in=item_in, force=True
    )
    validate_create_provider_attrs(obj_in=item_in, db_item=item)
    assert len(item.regions) == 1
    assert item.regions.single() == db_region


def test_delete_item(db_provider: Provider) -> None:
    """Delete an existing Provider."""
    assert provider.remove(db_obj=db_provider)
    assert not provider.get(uid=db_provider.uid)


def test_delete_item_with_projects(db_provider_with_single_project: Provider) -> None:
    """Delete an existing Provider.

    On cascade delete projects.
    """
    db_project = db_provider_with_single_project.projects.single()
    assert provider.remove(db_obj=db_provider_with_single_project)
    assert not provider.get(uid=db_provider_with_single_project.uid)
    assert not project.get(uid=db_project.uid)


def test_delete_item_with_regions(db_provider_with_single_region: Provider) -> None:
    """Delete an existing Provider.

    On cascade delete regions.
    """
    db_region = db_provider_with_single_region.regions.single()
    assert provider.remove(db_obj=db_provider_with_single_region)
    assert not provider.get(uid=db_provider_with_single_region.uid)
    assert not region.get(uid=db_region.uid)


def test_delete_item_with_proprietary_idp(
    db_provider_with_single_idp: Provider,
) -> None:
    """Delete an existing Provider.

    Delete identity providers only if no other providers use them.
    """
    db_idp = db_provider_with_single_idp.identity_providers.single()
    assert provider.remove(db_obj=db_provider_with_single_idp)
    assert not provider.get(uid=db_provider_with_single_idp.uid)
    assert not identity_provider.get(uid=db_idp.uid)


def test_delete_item_with_shared_idp(db_provider_with_shared_idp: Provider) -> None:
    """Delete an existing Provider.

    Delete identity providers only if no other providers use them.
    """
    db_idp = db_provider_with_shared_idp.identity_providers.single()
    assert provider.remove(db_obj=db_provider_with_shared_idp)
    assert not provider.get(uid=db_provider_with_shared_idp.uid)
    assert identity_provider.get(uid=db_idp.uid)
