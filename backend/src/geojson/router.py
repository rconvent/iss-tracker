import logging
from typing import List

from fastapi import APIRouter, HTTPException
from src.geojson.schemas import GeojsonResponseIn, GeojsonResponseOut
from src.geojson.service import (
    delete_geojson_data_by_id,
    insert_geojson_data,
    select_geojson_data,
    select_geojson_data_by_id,
    select_geojson_data_by_type,
    select_geojson_data_by_uuid,
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{id}/", response_model=GeojsonResponseOut)
async def get_geojson_by_id(id: int) -> dict[str, str]:

    data = await select_geojson_data_by_id(id=id)
    if not data :
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "id": data["id"],               
        "type": data["type"],
        "geometry": data["geometry"],
        "properties": data["properties"],
    }

@router.delete("/{id}/")
async def delete_geojson_by_id(id: int) -> dict[str, str]:

    data = await select_geojson_data_by_id(id=id)
    if data :
        await delete_geojson_data_by_id(id=id)
        return {
            "msg": f"record with {id} deleted"
        }
    else :
        raise HTTPException(status_code=404, detail="Item not found")


@router.get("/", response_model=List[GeojsonResponseOut] | GeojsonResponseOut)
async def get_geojson(limit: int = 0, type: str | None = None, uuid:str | None = None) -> list[dict[str, str]] | dict[str, str]:

    if uuid:
        data = await select_geojson_data_by_uuid(uuid=uuid)
        if not data :
            raise HTTPException(status_code=404, detail="Item not found")
        return {
            "id": data["id"],
            "mapbox_uuid": data["mapbox_uuid"],               
            "type": data["type"],
            "geometry": data["geometry"],
            "properties": data["properties"],
        }

    if type :
        records = await select_geojson_data_by_type(type=type, limit=limit)
    else :
        records = await select_geojson_data(limit=limit)

    if not records :
        raise HTTPException(status_code=404, detail="Item not found")

    return [{
        "id": data["id"],
        "mapbox_uuid": data["mapbox_uuid"],               
        "type": data["type"],
        "geometry": data["geometry"],
        "properties": data["properties"],
    } for data in records]

    
@router.post("/", response_model=GeojsonResponseOut)
async def post_geojson(geojson_data: GeojsonResponseIn) -> dict[str, str]:

    data = await insert_geojson_data(geojson_data)
    if not data :
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "id": data["id"], 
        "mapbox_uuid": data["mapbox_uuid"],               
        "type": data["type"],
        "geometry": data["geometry"],
        "properties": data["properties"],
    }
    
