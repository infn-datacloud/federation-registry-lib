from fastapi import HTTPException, status
from typing import Any, List


def find_duplicates(items: List[Any], attr: str) -> None:
    seen = set()
    values = [j.__getattribute__(attr) for j in items]
    dupes = [x for x in values if x in seen or seen.add(x)]
    if len(dupes) > 0:
        duplicates = ",".join(dupes)
        msg = f"There are multiple items with identical {attr}: "
        msg += f"{duplicates}"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )
