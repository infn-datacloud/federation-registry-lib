from ..available_vm_image.schemas import (
    AvailableVMImage,
    AvailableVMImageCreate,
)
from ..image.schemas import Image, ImageCreate


class ImageCreateExtended(ImageCreate):
    relationship: AvailableVMImageCreate


class ImageExtended(Image):
    relationship: AvailableVMImage
