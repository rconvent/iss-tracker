from databases.interfaces import Record
from fastapi import APIRouter, HTTPException, status
from src.iss.schemas import ISSResponseIn, ISSResponseOut
from src.iss.service import add_iss_data, get_last_iss_data

router = APIRouter()


@router.get("/position/", response_model=ISSResponseOut)
async def get_iss_position() -> dict[str, str]:

    data = await get_last_iss_data()
    if not data :
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "id": data["id"],               # type: ignore
        "name": data["name"],           # type: ignore
        "latitude": data["latitude"],   # type: ignore
        "longitude": data["longitude"], # type: ignore
        "altitude": data["altitude"],   # type: ignore
        "velocity": data["velocity"],   # type: ignore
        "visibility": data["visibility"], # type: ignore
        "footprint": data["footprint"], # type: ignore
        "daynum": data["daynum"],       # type: ignore
        "timestamp": data["timestamp"], # type: ignore
        "solar_lat": data["solar_lat"], # type: ignore
        "solar_lon": data["solar_lon"], # type: ignore
        "units": data["units"],         # type: ignore
    }
    

@router.post("/position/", status_code=status.HTTP_201_CREATED, response_model=ISSResponseOut)
async def post_iss_position(iss_data: ISSResponseIn) -> dict[str, str]:
    data = await add_iss_data(iss_data)
    return {
        "id": data["id"],               # type: ignore
        "name": data["name"],           # type: ignore
        "latitude": data["latitude"],   # type: ignore
        "longitude": data["longitude"], # type: ignore
        "altitude": data["altitude"],   # type: ignore
        "velocity": data["velocity"],   # type: ignore
        "visibility": data["visibility"], # type: ignore
        "footprint": data["footprint"], # type: ignore
        "daynum": data["daynum"],       # type: ignore
        "timestamp": data["timestamp"], # type: ignore
        "solar_lat": data["solar_lat"], # type: ignore
        "solar_lon": data["solar_lon"], # type: ignore
        "units": data["units"],         # type: ignore

    }