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
    """Create a Provider, with linked projects, identity providers and
    regions."""
    item_in = create_random_provider(
        with_projects=True, with_identity_providers=True, with_regions=True
    )
    item = provider.create(obj_in=item_in)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_provider: Provider) -> None:
    """Retrieve a Provider from its UID."""
    item = provider.get(uid=db_provider.uid)
    assert item.uid == db_provider.uid


def test_get_non_existing_item() -> None:
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
    sorted_items = list(sorted(provider.get_multi(), key=lambda x: x.uid))

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
    relationships."""
    patch_in = create_random_provider_patch()
    item = provider.update(db_obj=db_provider, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_provider: Provider) -> None:
    """Try to update the attributes of an existing Provider, without updating
    its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
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


def test_forced_update_item_with_projects(setup_and_teardown_db: Generator) -> None:
    """Update the attributes and relationships of an existing Provider.

    At first update a Provider with a set of projects, updating its
    attributes and removing the existing projects.

    Update a Provider with no projects, changing its attributes and
    linking new projects.

    Update a Provider with a set of projects, changing both its
    attributes and replacing the existing projects with a new ones.

    Update a Provider with a set of projects, changing only its
    attributes leaving untouched its connections (this is different from
    the previous test because the flag force is set to True).
    """
    item_in = create_random_provider(with_projects=True)
    item = provider.create(obj_in=item_in)
    item_in = create_random_provider()
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider(with_projects=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider(with_projects=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)

    projects = item_in.projects
    item_in = create_random_provider()
    item_in.projects = projects
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects_and_identity_providers(
    setup_and_teardown_db: Generator,
) -> None:
    """Update the attributes and relationships of an existing Provider.

    At first update a Provider with a set of identity providers,
    updating its attributes and removing the existing identity
    providers.

    Update a Provider with no identity providers, changing its
    attributes and linking new identity providers.

    Update a Provider with a set of identity providers, changing both
    its attributes and replacing the existing identity providers with a
    new ones.

    Update a Provider with a set of identity providers, changing only
    its attributes leaving untouched its connections (this is different
    from the previous test because the flag force is set to True).
    """
    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item = provider.create(obj_in=item_in)
    item_in = create_random_provider()
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)

    projects = item_in.projects
    identity_providers = item_in.identity_providers
    item_in = create_random_provider()
    item_in.projects = projects
    item_in.identity_providers = identity_providers
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects_and_regions(
    setup_and_teardown_db: Generator,
) -> None:
    """Update the attributes and relationships of an existing Provider.

    At first update a Provider with a set of regions, updating its
    attributes and removing the existing regions.

    Update a Provider with no regions, changing its attributes and
    linking new regions.

    Update a Provider with a set of regions, changing both its
    attributes and replacing the existing regions with a new ones.

    Update a Provider with a set of regions, changing only its
    attributes leaving untouched its connections (this is different from
    the previous test because the flag force is set to True).
    """
    item_in = create_random_provider(with_projects=True, with_regions=True)
    item = provider.create(obj_in=item_in)
    item_in = create_random_provider(with_projects=True, with_regions=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    item_in = create_random_provider(with_projects=True, with_regions=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider(with_projects=True, with_regions=True)
    item = provider.create(obj_in=item_in)
    item_in = create_random_provider()
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)

    projects = item_in.projects
    regions = item_in.regions
    item_in = create_random_provider()
    item_in.projects = projects
    item_in.regions = regions
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_provider_attrs(obj_in=item_in, db_item=item)


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
