from app.crud import CRUDBase
from app.image.models import Image
from app.image.schemas import (
    ImageCreate,
    ImageRead,
    ImageReadPublic,
    ImageReadShort,
    ImageUpdate,
)
from app.image.schemas_extended import ImageReadExtended, ImageReadExtendedPublic
from app.provider.models import Provider


class CRUDImage(
    CRUDBase[
        Image,
        ImageCreate,
        ImageUpdate,
        ImageRead,
        ImageReadPublic,
        ImageReadShort,
        ImageReadExtended,
        ImageReadExtendedPublic,
    ]
):
    """"""

    def create(
        self, *, obj_in: ImageCreate, provider: Provider, force: bool = False
    ) -> Image:
        db_obj = super().create(obj_in=obj_in, force=force)
        db_obj.provider.connect(provider)
        return db_obj


image = CRUDImage(
    model=Image,
    create_schema=ImageCreate,
    read_schema=ImageRead,
    read_public_schema=ImageReadPublic,
    read_short_schema=ImageReadShort,
    read_extended_schema=ImageReadExtended,
    read_extended_public_schema=ImageReadExtendedPublic,
)
