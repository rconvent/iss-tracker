import logging
from collections import defaultdict
from datetime import date

from fastapi import APIRouter, HTTPException, status
from src.iss.schemas import ISSResponseIn, ISSResponseOut
from src.iss.service import (
    insert_iss_data,
    retrieve_iss_sun_exposure,
    select_last_iss_data,
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/position/", response_model=ISSResponseOut)
async def get_iss_position() -> dict[str, str]:

    data = await select_last_iss_data()
    if not data :
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "id": data["id"],               
        "name": data["name"],           
        "latitude": data["latitude"],   
        "longitude": data["longitude"], 
        "altitude": data["altitude"],   
        "velocity": data["velocity"],   
        "visibility": data["visibility"], 
        "footprint": data["footprint"], 
        "daynum": data["daynum"],       
        "timestamp": data["timestamp"], 
        "solar_lat": data["solar_lat"], 
        "solar_lon": data["solar_lon"], 
        "units": data["units"],
    }
    

@router.get("/sun/", response_model=list[str])
async def get_iss_sun_exposure(from_date : date, to_date: date = date.today()) -> list[str] | None:

    records = await retrieve_iss_sun_exposure(from_date=from_date, to_date=to_date)    
    if not records :
        raise HTTPException(status_code=404, detail="No record found")

    sun_exposure: dict[int, list[str]] = defaultdict(list)
    window = -1
    visibility = "eclipsed"
    
    for record in records:
        if record["visibility"] == "visible" :
            continue
        
        if record["visibility"] == "daylight" and visibility == "eclipsed":
            window += 1
        
        visibility = record["visibility"]
        if visibility == "daylight":
            sun_exposure[window] += [record["timestamp"].strftime("%Y-%m-%d %H:%M:%S")]

    return [f"{exposure[0]} - {exposure[-1]}" for exposure in sun_exposure.values() if len(exposure) > 2]
