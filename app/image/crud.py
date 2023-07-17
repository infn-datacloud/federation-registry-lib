from app.image.models import Image as ImageModel
from app.image.schemas import ImageCreate, ImageUpdate
from app.crud import CRUDBase


class CRUDImage(CRUDBase[ImageModel, ImageCreate, ImageUpdate]):
    """"""


image = CRUDImage(ImageModel, ImageCreate)
