from .models import Image as ImageModel
from .schemas import ImageCreate, ImagePatch
from ..crud import CRUDBase


class CRUDImage(CRUDBase[ImageModel, ImageCreate, ImagePatch]):
    """"""


image = CRUDImage(ImageModel, ImageCreate)
