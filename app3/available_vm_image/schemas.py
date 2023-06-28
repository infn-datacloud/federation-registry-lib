from ..models import (
    BaseProviderRelCreate,
    BaseProviderRelQuery,
    BaseProviderRelRead,
)


class AvailableVMImageQuery(BaseProviderRelQuery):
    """AvailableVMImage Query Model class.

    Attributes:
        uuid (UUID4 | None): unique identifier of this item
            given by the provider.
        name (str | None): unique name of this item
            given by the provider.
    """


class AvailableVMImageCreate(BaseProviderRelCreate):
    """AvailableVMImage Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        uuid (UUID4): unique identifier of this item
            given by the provider.
        name (str): unique name of this item
            given by the provider.
    """


class AvailableVMImageUpdate(BaseProviderRelCreate):
    """AvailableVMImage Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        uuid (UUID4 | None): unique identifier of this item
            given by the provider.
        name (str | None): unique name of this item
            given by the provider.
    """


class AvailableVMImage(AvailableVMImageCreate, BaseProviderRelRead):
    """AvailableVMImage class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uuid (UUID4): unique identifier of this item
            given by the provider.
        name (str): unique name of this item
            given by the provider.
    """
