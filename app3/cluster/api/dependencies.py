from fastapi import HTTPException, status
from pydantic import UUID4

from ..crud import read_cluster
from ..models import Cluster


def valid_cluster_id(cluster_uid: UUID4) -> Cluster:
    item = read_cluster(uid=str(cluster_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cluster {cluster_uid} not found",
        )
    return item