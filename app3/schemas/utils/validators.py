from datetime import datetime
from neo4j.time import DateTime

def cast_neo4j_datetime(v: DateTime) -> datetime:
    """Convert neo4j datetime to datetime"""
    if type(v) is DateTime:
        return v.to_native()
    return v