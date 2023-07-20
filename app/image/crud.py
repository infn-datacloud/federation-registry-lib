from app.crud import CRUDBase
from app.image.models import Image 
from app.image.schemas import ImageCreate, ImageUpdate


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    """"""


image = CRUDImage(Image, ImageCreate)
