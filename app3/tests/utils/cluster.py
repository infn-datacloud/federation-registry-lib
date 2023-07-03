from .utils import random_lower_string
from ...cluster.crud import cluster
from ...cluster.models import Cluster
from ...cluster.schemas import ClusterCreate, ClusterUpdate


def create_random_cluster() -> Cluster:
    description = random_lower_string()
    item_in = ClusterCreate(description=description)
    return cluster.create(obj_in=item_in)


def create_random_update_cluster_data() -> ClusterUpdate:
    description = random_lower_string()
    return ClusterUpdate(description=description)
