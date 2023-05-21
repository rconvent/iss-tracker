import logging
from datetime import date, datetime

from databases.interfaces import Record
from pydantic import UUID4
from sqlalchemy import asc, desc, insert, select
from src import utils
from src.database import database, iss_data
from src.iss.schemas import ISSResponseIn

logger = logging.getLogger(__name__)

async def insert_iss_data(data: ISSResponseIn) -> Record | None :
    insert_query = (
        insert(iss_data)
        .values(
            {
                "id": data.id,
                "name": data.name,
                "latitude": data.latitude,
                "longitude": data.longitude,
                "altitude": data.altitude,
                "velocity": data.velocity,
                "visibility": data.visibility,
                "footprint": data.footprint,
                "daynum": data.daynum,
                "timestamp": datetime.fromtimestamp(data.timestamp),
                "solar_lat": data.solar_lat,
                "solar_lon": data.solar_lon,
                "units": data.units,
            }
        )
        .returning(iss_data)
    )

    return await database.fetch_one(insert_query)

async def select_last_iss_data() -> Record | None:
    select_query = select(iss_data).order_by(desc(iss_data.c.timestamp))

    return await database.fetch_one(select_query)

async def retrieve_iss_sun_exposure(from_date: date, to_date:date) -> list[Record] | None :
    select_query = select(iss_data.c.timestamp, iss_data.c.visibility).where(iss_data.c.timestamp >= from_date)
    select_query = select_query.where(iss_data.c.timestamp <= to_date).order_by(asc(iss_data.c.timestamp))

    return await database.fetch_all(select_query)