from .models import Cluster as ClusterModel
from .schemas import ClusterCreate, ClusterPatch
from ..crud import CRUDBase


class CRUDCluster(CRUDBase[ClusterModel, ClusterCreate, ClusterPatch]):
    """"""


cluster = CRUDCluster(ClusterModel, ClusterCreate)
