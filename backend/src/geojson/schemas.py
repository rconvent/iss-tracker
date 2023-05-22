from datetime import datetime
from enum import Enum
from typing import Any, Dict, TypeVar, Union

from geojson_pydantic.geometries import Geometry, GeometryCollection
from pydantic import Field
from src.models import ORJSONModel


class GEOMETRYTYPE(str, Enum):
    FEATURE = "Feature"
    MULTIPOINT = "MultiPoint"
    LINESTRING = "LineString"
    POLYGON = "Polygon"

class TYPE(str, Enum):
    FEATURE = "Feature"


    
class GeojsonResponseIn(ORJSONModel):
    type: TYPE
    # geometry:  Union[Geometry, GeometryCollection]
    geometry: Dict[str, Any]
    properties: Dict[str, Any]

class GeojsonResponseOut(ORJSONModel):
    id: int 
    type: TYPE
    geometry:  Union[Geometry, GeometryCollection]
    properties: Dict[str, Any]




