from typing import Any

USAGE_IDX = 2
PER_USER_IDX = 1
PROJECT_IDX = 0
MAX_Q = 2


def find_duplicates(items: Any, attr: str | None = None) -> None:
    """Find duplicate items in a list.

    Optionally filter items by attribute
    """
    if attr:
        values = [j.__getattribute__(attr) for j in items]
    else:
        values = items
    seen = set()
    dupes = [x for x in values if x in seen or seen.add(x)]
    if attr:
        assert len(dupes) == 0, (
            f"There are multiple items with identical {attr}: {','.join(dupes)}"
        )
    else:
        assert len(dupes) == 0, f"There are multiple identical items: {','.join(dupes)}"


def multiple_quotas_same_project(quotas: list[Any]) -> None:
    """Verify maximum number of quotas on same project.

    A project can have at most one `project` quota, one `per-user` quota and one `usage`
    quota on a specific service.
    """
    d = {}
    for quota in quotas:
        msg = f"Multiple quotas on same project {quota.project}"
        if not d.get(quota.project, None):
            d[quota.project] = [0, 0, 0]
        if quota.usage:
            d[quota.project][USAGE_IDX] += 1
        elif quota.per_user:
            d[quota.project][PER_USER_IDX] += 1
        else:
            d[quota.project][PROJECT_IDX] += 1
        assert (
            d[quota.project][PROJECT_IDX] < MAX_Q
            and d[quota.project][PER_USER_IDX] < MAX_Q
            and d[quota.project][USAGE_IDX] < MAX_Q
        ), msg
