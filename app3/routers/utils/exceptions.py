from fastapi import HTTPException, status

HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Cluster not found"
)
