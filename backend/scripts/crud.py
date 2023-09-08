from typing import Dict, Generic, List, TypeVar

import requests
from fastapi import status
from fastapi.encoders import jsonable_encoder
from logger import logger
from pydantic import AnyHttpUrl, BaseModel

WriteSchema = TypeVar("WriteSchema", bound=BaseModel)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)


class CRUDBase(Generic[WriteSchema, ReadSchema]):
    def __init__(self, type: str) -> None:
        super().__init__()
        self.type = type.capitalize()

    def __action_failed(
        self, *, resp: requests.Response, name: str, action: str
    ) -> None:
        logger.error(f"Failed to {action} {self.type.lower()} '{name}'")
        logger.error(f"Status code: {resp.status_code}")
        logger.error(f"Message: {resp.text}")

    def create(
        self, *, new_data: WriteSchema, url: AnyHttpUrl, header: Dict[str, str]
    ) -> None:
        resp = requests.post(url=url, json=jsonable_encoder(new_data), headers=header)
        if resp.status_code == status.HTTP_201_CREATED:
            logger.info(f"{self.type} '{new_data.name}' successfully created")
        else:
            self.__action_failed(name=new_data.name, resp=resp, action="create")

    def update(
        self, *, new_data: WriteSchema, url: AnyHttpUrl, header: Dict[str, str]
    ) -> None:
        resp = requests.patch(url=url, json=jsonable_encoder(new_data), headers=header)
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{self.type} '{new_data.name}' successfully updated")
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info("New data match stored data.")
            logger.info(f"{self.type} '{new_data.name}' not modified")
        else:
            self.__action_failed(name=new_data.name, resp=resp, action="update")

    def find(self, *, new_data: WriteSchema, db_items: List[ReadSchema]) -> ReadSchema:
        db_item = None
        if new_data.name in [i.name for i in db_items]:
            idx = [i.name for i in db_items].index(new_data.name)
            db_item = db_items[idx]
            logger.info(
                f"{self.type} '{new_data.name}' already belongs to this provider"
            )
        elif new_data.uuid in [i.uuid for i in db_items]:
            idx = [i.uuid for i in db_items].index(new_data.uuid)
            db_item = db_items[idx]
            logger.info(
                f"{self.type} '{new_data.uuid}' already belongs to this provider"
            )
        else:
            logger.info(
                f"No {self.type.lower()}s with name '{new_data.name}' "
                f"or uuid '{new_data.uuid}' belongs to this provider"
            )
        return db_item
