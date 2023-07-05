from .models import Image as ImageModel
from .schemas import ImageCreate, ImageUpdate
from ..crud import CRUDBase


class CRUDImage(CRUDBase[ImageModel, ImageCreate, ImageUpdate]):
    """"""


image = CRUDImage(ImageModel, ImageCreate)
