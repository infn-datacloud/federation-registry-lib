from typing import Any, Callable, List, Optional
from neomodel import StructuredNode, RelationshipManager
from pydantic import BaseModel


def check_rel_name_uuid_consist_connection(
    rel_manager: RelationshipManager, new_end_node: BaseModel
):
    end_node_rel_match_name = rel_manager.match(
        name=new_end_node.relationship.name
    ).all()
    end_node_rel_match_uuid = rel_manager.match(
        uuid=new_end_node.relationship.uuid
    ).all()

    if len(end_node_rel_match_name) > 1:
        raise  # TODO
    elif len(end_node_rel_match_name) == 1:
        end_node_rel_match_name = end_node_rel_match_name[0]
    else:
        end_node_rel_match_name = None
    if len(end_node_rel_match_uuid) > 1:
        raise  # TODO
    elif len(end_node_rel_match_uuid) == 1:
        end_node_rel_match_uuid = end_node_rel_match_uuid[0]
    else:
        end_node_rel_match_uuid = None

    if end_node_rel_match_name != end_node_rel_match_uuid or (
        end_node_rel_match_name is not None
        and (
            rel_manager.relationship(end_node_rel_match_name).uuid
            != rel_manager.relationship(end_node_rel_match_uuid).uuid
            or rel_manager.relationship(end_node_rel_match_uuid).name
            != rel_manager.relationship(end_node_rel_match_name).name
        )
    ):
        if end_node_rel_match_name is not None:
            rel_manager.disconnect(end_node_rel_match_name)
        if end_node_rel_match_uuid is not None:
            rel_manager.disconnect(end_node_rel_match_uuid)
        return None

    return end_node_rel_match_name


def create_and_connect(
    rel_manager: RelationshipManager,
    new_end_node: BaseModel,
    read_func: Callable,
    create_func: Callable,
):
    db_clu = read_func(
        **new_end_node.dict(exclude={"relationship"}, exclude_none=True)
    )
    if db_clu is None:
        db_clu = create_func(new_end_node)
        rel_manager.connect(db_clu, new_end_node.relationship.dict())
    else:
        rel_manager.replace(db_clu, new_end_node.relationship.dict())


def create_and_replace(
    rel_manager: RelationshipManager,
    new_end_node: BaseModel,
    read_func: Callable,
    create_func: Callable,
):
    db_clu = read_func(
        **new_end_node.dict(exclude={"relationship"}, exclude_none=True)
    )
    if db_clu is None:
        db_clu = create_func(new_end_node)
        rel_manager.replace(db_clu, new_end_node.relationship.dict())
    else:
        rel_manager.connect(db_clu, new_end_node.relationship.dict())


def truncate(
    items: List[Any], skip: int = 0, limit: Optional[int] = None
) -> List[Any]:
    if limit is None:
        return items[skip:]
    start = skip
    end = skip + limit
    return items[start:end]


def update(new_item: BaseModel, old_item: StructuredNode):
    for k, v in new_item.dict(exclude_unset=True).items():
        old_item.__setattr__(k, v)
    old_item.save()
    return old_item
