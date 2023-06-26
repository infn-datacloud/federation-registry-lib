from ..available_cluster.schemas import (
    AvailableCluster,
    AvailableClusterCreate,
)
from .schemas import Cluster, ClusterCreate


class ClusterCreateExtended(ClusterCreate):
    relationship: AvailableClusterCreate


class ClusterExtended(Cluster):
    relationship: AvailableCluster
