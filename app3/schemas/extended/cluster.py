from ..nodes.cluster import Cluster, ClusterCreate
from ..relationships.available_cluster import AvailableCluster, AvailableClusterCreate


class ClusterCreateExtended(ClusterCreate):
    relationship: AvailableClusterCreate


class ClusterExtended(Cluster):
    relationship: AvailableCluster
