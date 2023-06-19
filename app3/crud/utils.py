from typing import Any, List, Optional


def truncate(
    items: List[Any], skip: int = 0, limit: Optional[int] = None
) -> List[Any]:
    if limit is None:
        return items[skip:]
    start = skip
    end = skip + limit
    return items[start:end]
