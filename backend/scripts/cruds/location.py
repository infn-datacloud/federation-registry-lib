from typing import Dict, Optional

from cruds.core import BasicCRUD
from models.cmdb.location import LocationQuery, LocationRead, LocationWrite
from models.cmdb.region import RegionRead
from models.config import URLs


class LocationCRUD(BasicCRUD[LocationWrite, LocationRead, LocationQuery]):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=LocationRead,
            write_schema=LocationWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.locations,
            parent_url=cmdb_urls.regions,
            connectable_items=["regions"],
        )

    def synchronize(
        self, *, item: LocationWrite, parent: RegionRead
    ) -> Optional[LocationRead]:
        if item is not None:
            db_item = self.single(data=LocationQuery(site=item.site))
            if db_item is None:
                new_data = self.create(data=item, parent_uid=parent.uid)
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
                self.connect(uid=new_data.uid, parent_uid=parent.uid)
            return new_data
        db_item = parent.location
        if item is None and db_item is not None:
            self.disconnect(uid=db_item.uid, parent_uid=parent.uid)
            # TODO Verify to delete all orphan locations
            return None
        return None
