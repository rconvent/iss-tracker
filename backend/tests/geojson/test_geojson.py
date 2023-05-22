import logging
from datetime import datetime

import pytest
from async_asgi_testclient import TestClient
from src.geojson.schemas import GeojsonResponseIn
from src.geojson.service import insert_geojson_data

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_insert_geojson_data(client: TestClient) -> None:
    data = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                1,
                2
            ],
            "bbox": None
        },
        "properties": {
            "name": "jeff"
        }
    }
    record = await insert_geojson_data(GeojsonResponseIn(**data))
    
    assert record is not None
    assert record["geometry"]["coordinates"] == [1,2] 


@pytest.mark.asyncio
async def test_get_geojson_API(client: TestClient) -> None:
    
    # Test posts
    data = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        100.0,
                        0.0
                    ],
                    [
                        101.0,
                        0.0
                    ],
                    [
                        101.0,
                        1.0
                    ],
                    [
                        100.0,
                        1.0
                    ],
                    [
                        100.0,
                        0.0
                    ]
                ]
            ]
        },
        "properties": {
            "prop0": "value0",
            "prop1": {
                "this": "that"
            }
        }
    }
    record_1 = await insert_geojson_data(GeojsonResponseIn(**data))
    assert record_1 is not None

    data = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                1,
                2
            ],
            "bbox": None
        },
        "properties": {
            "name": "jeff"
        }
    }
    record_2 = await insert_geojson_data(GeojsonResponseIn(**data))
    assert record_2 is not None

    # test get by id
    resp = await client.get(
        f"/geojson/{record_1['id']}",
    )
    assert resp.status_code == 200

    # test get by type
    resp = await client.get(
        '/geojson/?type="Point"',
    )
    assert resp.status_code == 200
    assert record_2['id'] in [geo.get("id") for geo in resp.json()]

    # test delete by id
    resp = await client.delete(
        f"/geojson/{record_1['id']}",
    )
    assert resp.status_code == 200


    





