from pydantic import BaseModel, root_validator
from typing import Optional


class CommonGetQuery(BaseModel):
    skip: int = 0
    limit: Optional[int] = None
    sort: Optional[str] = None

    @root_validator
    def must_end_with(cls, values):
        sort_rule = values["sort"]
        if sort_rule is None:
            return values

        if sort_rule.endswith("_asc"):
            new_val = sort_rule[: -len("_asc")]
        if sort_rule.endswith("_desc"):
            new_val = sort_rule[: -len("_desc")]
            new_val = f"-{new_val}"
        else:
            new_val = sort_rule

        values["sort"] = new_val
        return values
