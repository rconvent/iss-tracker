import logging
from datetime import datetime

import pytest
from async_asgi_testclient import TestClient
from src.iss.schemas import ISSResponseIn
from src.iss.service import insert_iss_data

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_sun_exposure(client: TestClient) -> None:
    base_data = {
            "name": "iss",
            "id": 25544,
            "latitude": 40,
            "longitude": -100,
            "altitude": 422,
            "velocity": 27587,
            "footprint": 4521,
            "daynum": 2460085.8234259,
            "solar_lat": 20,
            "solar_lon": 62,
            "units": "kilometers"
        }
    await insert_iss_data(ISSResponseIn(
        **base_data,
        **{
            "timestamp": datetime.timestamp(datetime.fromisoformat("2021-10-01 12:00:00")),
            "visibility": "daylight"
        }
    ))
    await insert_iss_data(ISSResponseIn(
        **base_data,
        **{
            "timestamp": datetime.timestamp(datetime.fromisoformat("2021-10-01 12:10:00")),
            "visibility": "daylight"
        }
    ))
    await insert_iss_data(ISSResponseIn(
        **base_data,
        **{
            "timestamp": datetime.timestamp(datetime.fromisoformat("2021-10-01 12:20:00")),
            "visibility": "daylight"
        }
    ))
    await insert_iss_data(ISSResponseIn(
        **base_data,
        **{
            "timestamp": datetime.timestamp(datetime.fromisoformat("2021-10-01 12:30:00")),
            "visibility": "daylight"
        }
    ))
    await insert_iss_data(ISSResponseIn(
        **base_data,
        **{
            "timestamp": datetime.timestamp(datetime.fromisoformat("2021-10-01 12:40:00")),
            "visibility": "eclipsed"
        }
    ))
    await insert_iss_data(ISSResponseIn(
        **base_data,
        **{
            "timestamp": datetime.timestamp(datetime.fromisoformat("2021-10-01 12:50:00")),
            "visibility": "eclipsed"
        }
    ))
    await insert_iss_data(ISSResponseIn(
        **base_data,
        **{
            "timestamp": datetime.timestamp(datetime.fromisoformat("2021-10-01 13:00:00")),
            "visibility": "eclipsed"
        }
    ))
    await insert_iss_data(ISSResponseIn(
        **base_data,
        **{
            "timestamp": datetime.timestamp(datetime.fromisoformat("2021-10-01 13:10:00")),
            "visibility": "daylight"
        }
    ))
    await insert_iss_data(ISSResponseIn(
        **base_data,
        **{
            "timestamp": datetime.timestamp(datetime.fromisoformat("2021-10-01 13:20:00")),
            "visibility": "visible"
        }
    ))
    recod = await insert_iss_data(ISSResponseIn(
        **base_data,
        **{
            "timestamp": datetime.timestamp(datetime.fromisoformat("2021-10-01 14:30:00")),
            "visibility": "daylight"
        }
    ))
    print(recod)

    resp = await client.get(
        "/iss/sun/?from_date=2021-10-01&to_date=2021-10-02",
    )
    resp_json = resp.json()
    assert resp.status_code == 200
    assert resp_json == ['2021-10-01 12:00:00 - 2021-10-01 12:30:00', '2021-10-01 13:10:00 - 2021-10-01 14:30:00']




@pytest.mark.asyncio
async def test_insert_iss_data() -> None:
    data = {
            "name": "iss",
            "id": 25544,
            "latitude": 40,
            "longitude": -100,
            "altitude": 422,
            "velocity": 100000,
            "visibility": "daylight",
            "footprint": 4521,
            "timestamp": datetime.timestamp(datetime.now()),
            "daynum": 2460085.8234259,
            "solar_lat": 20,
            "solar_lon": 62,
            "units": "kilometers"
        }
    record = await insert_iss_data(ISSResponseIn(**data))
    
    assert record is not None
    assert record["velocity"] == 100000 


@pytest.mark.asyncio
async def test_get_iss_position(client: TestClient) -> None:
    resp = await client.get(
        "/iss/position"
    )
    assert resp.status_code == 200
    assert resp.json().get("velocity") == 100000 





