from app.crud import CRUDBase
from app.image.models import Image
from app.image.schemas import ImageCreate, ImageUpdate
from app.provider.models import Provider


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    """"""

    def create(
        self, *, obj_in: ImageCreate, provider: Provider, force: bool = False
    ) -> Image:
        db_obj = super().create(obj_in=obj_in, force=force)
        db_obj.provider.connect(provider)
        return db_obj


image = CRUDImage(Image, ImageCreate)
