from .utils import random_lower_string
from ...cluster.crud import cluster
from ...cluster.models import Cluster
from ...cluster.schemas import ClusterCreate


def create_random_cluster() -> Cluster:
    description = random_lower_string()
    item_in = ClusterCreate(description=description)
    return cluster.create(obj_in=item_in)
