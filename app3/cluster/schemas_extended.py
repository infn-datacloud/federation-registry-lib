from ..available_cluster.schemas import (
    AvailableCluster,
    AvailableClusterCreate,
    AvailableClusterUpdate,
)
from .schemas import Cluster, ClusterCreate, ClusterUpdate


class ClusterCreateExtended(ClusterCreate):
    relationship: AvailableClusterCreate


class ClusterUpdateExtended(ClusterUpdate):
    relationship: AvailableClusterUpdate


class ClusterExtended(Cluster):
    relationship: AvailableCluster
