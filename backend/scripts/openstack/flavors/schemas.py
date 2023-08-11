from pydantic import Field

from scripts.openstack.schemas import OpenstackItem


class Flavor(OpenstackItem):
    ram: int = Field(description="The amount of RAM a flavor has, in MiB.")
    disk: int = Field(
        description="The size of the root disk that will be created in GiB."
    )
    vcpus: int = Field(
        description="The number of virtual CPUs that will be allocated to the server."
    )
    ephemeral_disk: int = Field(
        description="The size of the ephemeral disk that will be created, in GiB."
    )
    swap: int = Field(
        description="The size of a dedicated swap disk that will be allocated, in MiB."
    )
    is_public: bool = Field(
        description="Whether the flavor is public (available to all projects) \
            or scoped to a set of projects."
    )

    def __init__(self, **kwargs):  # TODO evaluate usage of alias
        kwargs["ephemeral_disk"] = kwargs["OS-FLV-EXT-DATA:ephemeral"]
        kwargs["is_public"] = kwargs["os-flavor-access:is_public"]
        super().__init__(**kwargs)
