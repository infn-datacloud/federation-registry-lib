from .models import Cluster as ClusterModel
from .schemas import ClusterCreate, ClusterUpdate
from ..crud import CRUDBase


class CRUDCluster(CRUDBase[ClusterModel, ClusterCreate, ClusterUpdate]):
    """"""


cluster = CRUDCluster(ClusterModel, ClusterCreate)
