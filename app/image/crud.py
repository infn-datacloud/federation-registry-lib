from app.image.models import Image 
from app.image.schemas import ImageCreate, ImageUpdate
from app.crud import CRUDBase


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    """"""


image = CRUDImage(Image, ImageCreate)
