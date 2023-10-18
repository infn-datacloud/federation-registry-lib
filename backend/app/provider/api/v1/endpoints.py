from typing import List, Optional, Union

from app.auth.dependencies import check_read_access, check_write_access
from app.auth_method.schemas import AuthMethodCreate
from app.identity_provider.api.dependencies import (
    valid_identity_provider_endpoint,
    valid_identity_provider_id,
)
from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import IdentityProviderCreate
from app.identity_provider.schemas_extended import IdentityProviderReadExtended
from app.project.api.dependencies import valid_project_name, valid_project_uuid
from app.project.crud import project
from app.project.schemas import ProjectCreate
from app.project.schemas_extended import ProjectReadExtended
from app.provider.api.dependencies import (
    valid_provider,
    valid_provider_id,
    validate_new_provider_values,
)
from app.provider.crud import provider
from app.provider.models import Provider
from app.provider.schemas import (
    ProviderQuery,
    ProviderRead,
    ProviderReadPublic,
    ProviderReadShort,
    ProviderUpdate,
)
from app.provider.schemas_extended import (
    ProviderCreateExtended,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
)
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from app.service.api.dependencies import valid_service_endpoint
from app.service.crud import (
    block_storage_service,
    compute_service,
    identity_service,
    network_service,
)
from app.service.schemas import (
    BlockStorageServiceCreate,
    ComputeServiceCreate,
    IdentityServiceCreate,
    NetworkServiceCreate,
)
from app.service.schemas_extended import (
    BlockStorageServiceReadExtended,
    ComputeServiceReadExtended,
    IdentityServiceReadExtended,
)
from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db

router = APIRouter(prefix="/providers", tags=["providers"])


@db.read_transaction
@router.get(
    "/",
    response_model=Union[
        List[ProviderReadExtended],
        List[ProviderRead],
        List[ProviderReadShort],
        List[ProviderReadExtendedPublic],
        List[ProviderReadPublic],
    ],
    summary="Read all providers",
    description="Retrieve all providers stored in the database. \
        It is possible to filter on providers attributes and other \
        common query parameters.",
)
def get_providers(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: ProviderQuery = Depends(),
):
    items = provider.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = provider.paginate(items=items, page=page.page, size=page.size)
    return provider.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.write_transaction
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProviderReadExtended,
    dependencies=[Depends(check_write_access), Depends(valid_provider)],
    summary="Create provider",
    description="Create a provider and its related entities: \
        flavors, identity providers, images, location, \
        projects and services. \
        At first validate new provider values checking there are \
        no other items with the given *name*. \
        Moreover check the received lists do not contain duplicates.",
)
def post_provider(item: ProviderCreateExtended):
    return provider.create(obj_in=item, force=True)


@db.read_transaction
@router.get(
    "/{provider_uid}",
    response_model=Union[
        ProviderReadExtended,
        ProviderRead,
        ProviderReadShort,
        ProviderReadExtendedPublic,
        ProviderReadPublic,
    ],
    summary="Read a specific provider",
    description="Retrieve a specific provider using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_provider(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: Provider = Depends(valid_provider_id),
):
    return provider.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{provider_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[ProviderRead],
    dependencies=[Depends(check_write_access), Depends(validate_new_provider_values)],
    summary="Edit a specific provider",
    description="Update attribute values of a specific provider. \
        The target provider is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new provider values checking there are \
        no other items with the given *name*.",
)
def put_provider(
    update_data: ProviderUpdate,
    response: Response,
    item: Provider = Depends(valid_provider_id),
):
    db_item = provider.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{provider_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific provider",
    description="Delete a specific provider using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related flavors, images, projects \
        and services.",
)
def delete_providers(item: Provider = Depends(valid_provider_id)):
    if not provider.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


# @db.write_transaction
# @router.post(
#    "/{provider_uid}/flavors/",
#    response_model=FlavorReadExtended,
#    status_code=status.HTTP_201_CREATED,
#    dependencies=[
#        Depends(check_write_access),
#        Depends(valid_flavor_name),
#        Depends(valid_flavor_uuid),
#    ],
#    summary="Add new flavor to provider",
#    description="Create a flavor and connect it to a \
#        provider knowing it *uid*. \
#        If no entity matches the given *uid*, the endpoint \
#        raises a `not found` error. \
#        At first validate new flavor values checking there are \
#        no other items with the given *name* or *uuid*.",
# )
# def add_flavor_to_provider(
#    item: FlavorCreate,
#    provider: Provider = Depends(valid_provider_id),
# ):
#    return flavor.create(obj_in=item, provider=provider, force=True)
#


@db.write_transaction
@router.post(
    "/{provider_uid}/identity_providers/",
    status_code=status.HTTP_201_CREATED,
    response_model=IdentityProviderReadExtended,
    dependencies=[
        Depends(check_write_access),
        Depends(valid_identity_provider_endpoint),
    ],
    summary="Create location",
    description="Create a location. \
        At first validate new location values checking there are \
        no other items with the given *name*.",
)
def post_location(item: IdentityProviderCreate):
    return identity_provider.create(obj_in=item, force=True)


@db.write_transaction
@router.put(
    "/{provider_uid}/identity_providers/{identity_provider_uid}",
    response_model=Optional[ProviderReadExtended],
    dependencies=[Depends(check_write_access)],
    summary="Connect provider to identity provider",
    description="Connect a provider to a specific identity \
        provider knowing their *uid*s. \
        If no entity matches the given *uid*s, the endpoint \
        raises a `not found` error.",
)
def connect_provider_to_identity_providers(
    data: AuthMethodCreate,
    response: Response,
    item: Provider = Depends(valid_provider_id),
    identity_provider: IdentityProvider = Depends(valid_identity_provider_id),
):
    if item.identity_providers.is_connected(identity_provider):
        db_item = item.identity_providers.relationship(identity_provider)
        if all(
            [
                db_item.__getattribute__(k) == v
                for k, v in data.dict(exclude_unset=True).items()
            ]
        ):
            response.status_code = status.HTTP_304_NOT_MODIFIED
            return None
        item.identity_providers.disconnect(identity_provider)
    item.identity_providers.connect(identity_provider, data.dict())
    return item


@db.write_transaction
@router.delete(
    "/{provider_uid}/identity_providers/{identity_provider_uid}",
    response_model=Optional[ProviderReadExtended],
    dependencies=[Depends(check_write_access)],
    summary="Disconnect provider from identity provider",
    description="Disconnect a provider from a specific identity \
        provider knowing their *uid*s. \
        If no entity matches the given *uid*s, the endpoint \
        raises a `not found` error.",
)
def disconnect_provider_from_identity_providers(
    response: Response,
    item: Provider = Depends(valid_provider_id),
    identity_provider: IdentityProvider = Depends(valid_identity_provider_id),
):
    if not item.identity_providers.is_connected(identity_provider):
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return None
    item.identity_providers.disconnect(identity_provider)
    return item


# @db.write_transaction
# @router.post(
#    "/{provider_uid}/images/",
#    response_model=ImageReadExtended,
#    status_code=status.HTTP_201_CREATED,
#    dependencies=[
#        Depends(check_write_access),
#        Depends(valid_image_name),
#        Depends(valid_image_uuid),
#    ],
#    summary="Add new image to provider",
#    description="Create a image and connect it to a \
#        provider knowing it *uid*. \
#        If no entity matches the given *uid*, the endpoint \
#        raises a `not found` error. \
#        At first validate new image values checking there are \
#        no other items with the given *name* or *uuid*.",
# )
# def add_image_to_provider(
#    item: ImageCreate,
#    provider: Provider = Depends(valid_provider_id),
# ):
#    return image.create(obj_in=item, provider=provider, force=True)


@db.write_transaction
@router.post(
    "/{provider_uid}/projects/",
    response_model=ProjectReadExtended,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(check_write_access),
        Depends(valid_project_name),
        Depends(valid_project_uuid),
    ],
    summary="Add new project to provider",
    description="Create a project and connect it to a \
        provider knowing it *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        At first validate new project values checking there are \
        no other items with the given *name* or *uuid*.",
)
def add_project_to_provider(
    item: ProjectCreate,
    provider: Provider = Depends(valid_provider_id),
):
    return project.create(obj_in=item, provider=provider, force=True)


@db.write_transaction
@router.post(
    "/{provider_uid}/services/",
    response_model=Union[
        BlockStorageServiceReadExtended,
        IdentityServiceReadExtended,
        ComputeServiceReadExtended,
    ],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_write_access), Depends(valid_service_endpoint)],
    summary="Add new service to provider",
    description="Create a service and connect it to a \
        provider knowing it *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        At first validate new service values checking there are \
        no other items with the given *name* or *uuid*.",
)
def add_service_to_provider(
    item: Union[
        BlockStorageServiceCreate,
        IdentityServiceCreate,
        ComputeServiceCreate,
        NetworkServiceCreate,
    ],
    provider: Provider = Depends(valid_provider_id),
):
    if isinstance(item, BlockStorageServiceCreate):
        return block_storage_service.create(obj_in=item, provider=provider, force=True)
    if isinstance(item, ComputeServiceCreate):
        return compute_service.create(obj_in=item, provider=provider, force=True)
    if isinstance(item, IdentityServiceCreate):
        return identity_service.create(obj_in=item, provider=provider, force=True)
    if isinstance(item, NetworkServiceCreate):
        return network_service.create(obj_in=item, provider=provider, force=True)
