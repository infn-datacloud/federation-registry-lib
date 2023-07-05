from enum import Enum


class ServiceType(Enum):
    """Possible IaaS services types"""

    open_stack_nova: str = "org.openstack.nova"
    mesos: str = "eu.indigo-datacloud.mesos"
    chronos: str = "eu.indigo-datacloud.chronos"
    marathon: str = "eu.indigo-datacloud.marathon"
    kubernetes: str = "eu.deep.kubernetes"
    rucio: str = "eu.egi.storage-element"
    onedata: str = "eu.egi.cloud.storage-management.oneprovider"
