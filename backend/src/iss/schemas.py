from datetime import datetime
from enum import Enum

from pydantic import Field
from src.models import ORJSONModel


class VISIBILITY(str, Enum):
    DAYLIGHT = "daylight"
    ECLIPSED = "eclipsed"

class UNITS(str, Enum):
    KILOMETERS = "kilometers"
    MILES = "miles"

    
class ISSResponseIn(ORJSONModel):
    name: str = Field(min_length=1, max_length=128)
    id: int 
    latitude: float = Field(le=90, ge=-90)
    longitude: float = Field(le=180 , ge=-180)
    altitude: float = Field(ge=0)
    velocity: float = Field(ge=0)
    visibility: VISIBILITY
    footprint: float
    timestamp: int
    daynum: float
    solar_lat: float 
    solar_lon: float 
    units: UNITS

class ISSResponseOut(ORJSONModel):
    name: str = Field(min_length=1, max_length=128)
    id: int 
    latitude: float = Field(le=90, ge=-90)
    longitude: float = Field(le=180 , ge=-180)
    altitude: float = Field(ge=0)
    velocity: float = Field(ge=0)
    visibility: VISIBILITY
    footprint: float
    timestamp: datetime
    daynum: float
    solar_lat: float 
    solar_lon: float 
    units: UNITS


