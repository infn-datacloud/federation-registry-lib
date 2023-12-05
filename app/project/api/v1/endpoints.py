from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPBasicCredentials
from neomodel import db

from app.auth import flaat, security

# from app.flavor.api.dependencies import is_private_flavor, valid_flavor_id
# from app.flavor.crud import flavor
# from app.flavor.models import Flavor
# from app.flavor.schemas import FlavorRead, FlavorReadPublic, FlavorReadShort
# from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
# from app.image.api.dependencies import is_private_image, valid_image_id
# from app.image.crud import image
# from app.image.models import Image
# from app.image.schemas import ImageRead, ImageReadPublic, ImageReadShort
# from app.image.schemas_extended import ImageReadExtended, ImageReadExtendedPublic
from app.project.api.dependencies import (
    valid_project_id,
    validate_new_project_values,
)
from app.project.api.utils import filter_on_region_attr
from app.project.crud import project
from app.project.models import Project
from app.project.schemas import (
    ProjectQuery,
    ProjectRead,
    ProjectReadPublic,
    ProjectReadShort,
    ProjectUpdate,
)
from app.project.schemas_extended import (
    ProjectReadExtended,
    ProjectReadExtendedPublic,
)
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from app.region.schemas import RegionQuery

router = APIRouter(prefix="/projects", tags=["projects"])


@db.read_transaction
@router.get(
    "/",
    response_model=Union[
        List[ProjectReadExtended],
        List[ProjectRead],
        List[ProjectReadShort],
        List[ProjectReadExtendedPublic],
        List[ProjectReadPublic],
    ],
    summary="Read all projects",
    description="Retrieve all projects stored in the database. \
        It is possible to filter on projects attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_projects(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: ProjectQuery = Depends(),
    region_name: Optional[str] = None,
    user_infos: Optional[Any] = None,
):
    items = project.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = project.paginate(items=items, page=page.page, size=page.size)
    region_query = RegionQuery(name=region_name)
    items = filter_on_region_attr(items=items, region_query=region_query)
    return project.choose_out_schema(
        items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{project_uid}",
    response_model=Union[
        ProjectReadExtended,
        ProjectRead,
        ProjectReadShort,
        ProjectReadExtendedPublic,
        ProjectReadPublic,
    ],
    summary="Read a specific project",
    description="Retrieve a specific project using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_project(
    size: SchemaSize = Depends(),
    item: Project = Depends(valid_project_id),
    region_name: Optional[str] = None,
    user_infos: Optional[Any] = None,
):
    region_query = RegionQuery(name=region_name)
    items = filter_on_region_attr(items=[item], region_query=region_query)
    items = project.choose_out_schema(
        items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
    )
    return items[0]


@db.write_transaction
@router.patch(
    "/{project_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[ProjectRead],
    dependencies=[
        Depends(validate_new_project_values),
    ],
    summary="Edit a specific project",
    description="Update attribute values of a specific project. \
        The target project is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new project values checking there are \
        no other items with the given *uuid* and *name*.",
)
@flaat.access_level("write")
def put_project(
    request: Request,
    update_data: ProjectUpdate,
    response: Response,
    item: Project = Depends(valid_project_id),
    client_credentials: HTTPBasicCredentials = Depends(security),
):
    db_item = project.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{project_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific project",
    description="Delete a specific project using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related SLA and quotas. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
@flaat.access_level("write")
def delete_project(
    request: Request,
    item: Project = Depends(valid_project_id),
    client_credentials: HTTPBasicCredentials = Depends(security),
):
    if not project.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


# @db.read_transaction
# @router.get(
#     "/{project_uid}/flavors",
#     response_model=Union[
#         List[FlavorReadExtended],
#         List[FlavorRead],
#         List[FlavorReadShort],
#         List[FlavorReadExtendedPublic],
#         List[FlavorReadPublic],
#     ],
#     summary="Read user group accessible flavors",
#     description="Retrieve all the flavors the user group \
#         has access to thanks to its SLA. \
#         If no entity matches the given *uid*, the endpoint \
#         raises a `not found` error.",
# )
# def get_project_flavors(
#     auth: bool = Depends(check_read_access),
#     size: SchemaSize = Depends(),
#     item: Project = Depends(valid_project_id),
# ):
#     items = item.private_flavors.all() + item.public_flavors()
#     return flavor.choose_out_schema(
#         items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
#     )


# @db.write_transaction
# @router.put(
#     "/{project_uid}/flavors/{flavor_uid}",
#     response_model=Optional[List[FlavorRead]],
#
#     summary="Connect project to flavor",
#     description="Connect a project to a specific flavor \
#         knowing their *uid*s. \
#         If no entity matches the given *uid*s, the endpoint \
#         raises a `not found` error.",
# )
# def connect_project_to_flavor(
#     response: Response,
#     item: Project = Depends(valid_project_id),
#     flavor: Flavor = Depends(is_private_flavor),
# ):
#     if item.private_flavors.is_connected(flavor):
#         response.status_code = status.HTTP_304_NOT_MODIFIED
#         return None
#     item.private_flavors.connect(flavor)
#     return item.private_flavors.all()


# @db.write_transaction
# @router.delete(
#     "/{project_uid}/flavors/{flavor_uid}",
#     response_model=Optional[List[FlavorRead]],
#
#     summary="Disconnect project from flavor",
#     description="Disconnect a project from a specific flavor \
#         knowing their *uid*s. \
#         If no entity matches the given *uid*s, the endpoint \
#         raises a `not found` error.",
# )
# def disconnect_project_from_flavor(
#     response: Response,
#     item: Project = Depends(valid_project_id),
#     flavor: Flavor = Depends(valid_flavor_id),
# ):
#     if not item.private_flavors.is_connected(flavor):
#         response.status_code = status.HTTP_304_NOT_MODIFIED
#         return None
#     item.private_flavors.disconnect(flavor)
#     return item.private_flavors.all()


# @db.read_transaction
# @router.get(
#     "/{project_uid}/images",
#     response_model=Union[
#         List[ImageReadExtended],
#         List[ImageRead],
#         List[ImageReadShort],
#         List[ImageReadExtendedPublic],
#         List[ImageReadPublic],
#     ],
#     summary="Read user group accessible images",
#     description="Retrieve all the images the user group \
#         has access to thanks to its SLA. \
#         If no entity matches the given *uid*, the endpoint \
#         raises a `not found` error.",
# )
# def get_project_images(
#     auth: bool = Depends(check_read_access),
#     size: SchemaSize = Depends(),
#     item: Project = Depends(valid_project_id),
# ):
#     items = item.private_images.all() + item.public_images()
#     return image.choose_out_schema(
#         items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
#     )


# @db.write_transaction
# @router.put(
#     "/{project_uid}/images/{image_uid}",
#     response_model=Optional[List[ImageRead]],
#
#     summary="Connect project to image",
#     description="Connect a project to a specific image \
#         knowing their *uid*s. \
#         If no entity matches the given *uid*s, the endpoint \
#         raises a `not found` error.",
# )
# def connect_project_to_image(
#     response: Response,
#     item: Project = Depends(valid_project_id),
#     image: Image = Depends(is_private_image),
# ):
#     if item.private_images.is_connected(image):
#         response.status_code = status.HTTP_304_NOT_MODIFIED
#         return None
#     item.private_images.connect(image)
#     return item.private_images.all()


# @db.write_transaction
# @router.delete(
#     "/{project_uid}/images/{image_uid}",
#     response_model=Optional[List[ImageRead]],
#
#     summary="Disconnect project from image",
#     description="Disconnect a project from a specific image \
#         knowing their *uid*s. \
#         If no entity matches the given *uid*s, the endpoint \
#         raises a `not found` error.",
# )
# def disconnect_project_from_image(
#     response: Response,
#     item: Project = Depends(valid_project_id),
#     image: Image = Depends(valid_image_id),
# ):
#     if not item.private_images.is_connected(image):
#         response.status_code = status.HTTP_304_NOT_MODIFIED
#         return None
#     item.private_images.disconnect(image)
#     return item.private_images.all()
