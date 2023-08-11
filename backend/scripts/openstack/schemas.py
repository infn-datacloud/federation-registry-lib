from pydantic import UUID4, BaseModel, Field


class OpenstackItem(BaseModel):
    uuid: UUID4 = Field(description="Unique ID of the item inside openstack")
    name: str = Field(description="Item name")
    description: str = Field(default="", description="Item description")

    def __init__(self, **kwargs):  # TODO evaluate usage of alias
        kwargs["uuid"] = kwargs["id"]
        super().__init__(**kwargs)
