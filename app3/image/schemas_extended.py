from ..available_vm_image.schemas import (
    AvailableVMImage,
    AvailableVMImageCreate,
    AvailableVMImageUpdate,
)
from ..image.schemas import Image, ImageCreate, ImageUpdate


class ImageCreateExtended(ImageCreate):
    relationship: AvailableVMImageCreate


class ImageUpdateExtended(ImageUpdate):
    relationship: AvailableVMImageUpdate


class ImageExtended(Image):
    relationship: AvailableVMImage
