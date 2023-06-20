from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class AvailableVMFlavorBase(BaseModel):
    """AvailableVMFlavor Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): AvailableVMFlavor name (type).
        description (str): Brief description.
        unit (str | None): Measurement unit derived from the
            quota name/type.
        tot_limit (float | None): The max quantity of a resource to
            be granted to the user group in total.
        instance_limit (float | None): The max quantity of a resource
            to be granted to each VM/Container instance.
        user_limit (float | None): The max quantity of a resource to
            be granted to user.
        tot_guaranteed (float): The guaranteed quantity of a
            resource to be granted to the user group in total.
        instance_guaranteed (float): The guaranteed quantity
            of a resource to be granted to each VM/Container
            instance.
        user_guaranteed (float): The guaranteed quantity
            of a resource to be granted to user.
    """

    name: Optional[str] = None
    uuid: Optional[UUID] = None

    class Config:
        validate_assignment = True


class AvailableVMFlavorUpdate(AvailableVMFlavorBase):
    """AvailableVMFlavor Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): AvailableVMFlavor name (type).
        description (str): Brief description.
        unit (str | None): Measurement unit derived from the
            quota name/type.
        tot_limit (float | None): The max quantity of a resource to
            be granted to the user group in total.
        instance_limit (float | None): The max quantity of a resource
            to be granted to each VM/Container instance.
        user_limit (float | None): The max quantity of a resource to
            be granted to user.
        tot_guaranteed (float): The guaranteed quantity of a
            resource to be granted to the user group in total.
        instance_guaranteed (float): The guaranteed quantity
            of a resource to be granted to each VM/Container
            instance.
        user_guaranteed (float): The guaranteed quantity
            of a resource to be granted to user.
    """


class AvailableVMFlavorCreate(AvailableVMFlavorUpdate):
    """AvailableVMFlavor Create class

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.


    Attributes:
        name (str): AvailableVMFlavor name (type).
        description (str): Brief description.
        unit (str | None): Measurement unit derived from the
            quota name/type.
        tot_limit (float | None): The max quantity of a resource to
            be granted to the user group in total.
        instance_limit (float | None): The max quantity of a resource
            to be granted to each VM/Container instance.
        user_limit (float | None): The max quantity of a resource to
            be granted to user.
        tot_guaranteed (float): The guaranteed quantity of a
            resource to be granted to the user group in total.
        instance_guaranteed (float): The guaranteed quantity
            of a resource to be granted to each VM/Container
            instance.
        user_guaranteed (float): The guaranteed quantity
            of a resource to be granted to user.
    """

    name: str
    uuid: UUID


class AvailableVMFlavor(AvailableVMFlavorCreate):
    """AvailableVMFlavor class

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): AvailableVMFlavor unique ID.
        name (str): AvailableVMFlavor name (type).
        description (str): Brief description.
        unit (str | None): Measurement unit derived from the
            quota name/type.
        tot_limit (float | None): The max quantity of a resource to
            be granted to the user group in total.
        instance_limit (float | None): The max quantity of a resource
            to be granted to each VM/Container instance.
        user_limit (float | None): The max quantity of a resource to
            be granted to user.
        tot_guaranteed (float): The guaranteed quantity of a
            resource to be granted to the user group in total.
        instance_guaranteed (float): The guaranteed quantity
            of a resource to be granted to each VM/Container
            instance.
        user_guaranteed (float): The guaranteed quantity
            of a resource to be granted to user.
    """

    class Config:
        orm_mode = True
