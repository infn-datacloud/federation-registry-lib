from ..nodes.image import Image, ImageCreate
from ..relationships.available_vm_image import AvailableVMImage, AvailableVMImageCreate


class ImageCreateExtended(ImageCreate):
    relationship: AvailableVMImageCreate


class ImageExtended(Image):
    relationship: AvailableVMImage
