import logging
from typing import List

from databases.interfaces import Record
from pydantic import UUID4
from sqlalchemy import delete, insert, select
from src.database import database, geojson_data
from src.geojson.schemas import GeojsonResponseIn

logger = logging.getLogger(__name__)

async def insert_geojson_data(data: GeojsonResponseIn) -> Record | None :
    insert_query = (
        insert(geojson_data)
        .values(
            {
                "type": data.type,
                "geometry": data.geometry,
                "properties": data.properties,
            }
        )
        .returning(geojson_data)
    )

    return await database.fetch_one(insert_query)

async def select_geojson_data_by_id(id: int) -> Record | None:
    select_query = select(geojson_data).where(geojson_data.c.id==id)

    return await database.fetch_one(select_query)


async def delete_geojson_data_by_id(id: int) -> Record | None:
    delete_query = delete(geojson_data).where(geojson_data.c.id==id)

    return await database.fetch_one(delete_query)


async def select_geojson_data(limit: int) -> List[Record] | None:
    select_query = select(geojson_data)
    if limit :
        select_query = select_query.limit(limit)

    return await database.fetch_all(select_query)


async def select_geojson_data_by_type(type: str, limit:int) -> List[Record] | None:
    select_query = select(geojson_data).where(geojson_data.c.geometry["type"]==type)
    if limit :
        select_query = select_query.limit(limit)

    return await database.fetch_all(select_query)
