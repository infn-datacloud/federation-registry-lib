
@db.write_transaction
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=LocationReadExtended,
    dependencies=[Depends(check_write_access), Depends(valid_location_site)],
    summary="Create location",
    description="Create a location. \
        At first validate new location values checking there are \
        no other items with the given *site*.",
)
def post_location(item: LocationCreate):
    return location.create(obj_in=item, force=True)



@db.write_transaction
@router.put(
    "/{provider_uid}/locations/{location_uid}",
    response_model=Optional[ProviderReadExtended],
    dependencies=[Depends(check_write_access)],
    summary="Connect provider to location",
    description="Connect a provider to a specific location \
        knowing their *uid*s. \
        If the provider already has a \
        current location and the new one is different, \
        the endpoint replaces it with the new one, otherwise \
        it leaves the entity unchanged and returns a \
        `not modified` message. \
        If no entity matches the given *uid*s, the endpoint \
        raises a `not found` error.",
)
def connect_provider_to_location(
    response: Response,
    item: Provider = Depends(valid_provider_id),
    location: Location = Depends(valid_location_id),
):
    if item.location.single() is None:
        item.location.connect(location)
    elif not item.location.is_connected(location):
        item.location.replace(location)
    else:
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return None
    return item


@db.write_transaction
@router.delete(
    "/{provider_uid}/locations/{location_uid}",
    response_model=Optional[ProviderReadExtended],
    dependencies=[Depends(check_write_access)],
    summary="Disconnect provider from location",
    description="Disconnect a provider from a specific location \
        knowing their *uid*s. \
        If no entity matches the given *uid*s, the endpoint \
        raises a `not found` error.",
)
def disconnect_provider_from_location(
    response: Response,
    item: Provider = Depends(valid_provider_id),
    location: Location = Depends(valid_location_id),
):
    if not item.location.is_connected(location):
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return None
    item.location.disconnect(location)
    return item
