import logging

from databases import Database
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Identity,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.dialects.postgresql import JSONB
from src.config import settings
from src.constants import DB_NAMING_CONVENTION

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

database = Database(DATABASE_URL, force_rollback=settings.ENVIRONMENT.is_testing)

iss_data = Table(
    "iss_data",
    metadata,
    Column("id", Integer, Identity()),
    Column("name", String, nullable=False),
    Column("latitude", Float, nullable=False),
    Column("longitude", Float, nullable=False),
    Column("altitude", Float, nullable=False),
    Column("velocity", Float, nullable=False),
    Column("visibility", String, nullable=False),
    Column("footprint", Float, nullable=False),
    Column("daynum", Float, nullable=False),
    Column("timestamp", DateTime, nullable=False, index=True),
    Column("solar_lat", Float, nullable=False),
    Column("solar_lon", Float, nullable=False),
    Column("units", String, nullable=False),
)


geojson_data = Table(
    "geojson_data",
    metadata,
    Column("id", Integer, Identity(start=42, cycle=True), primary_key=True),
    Column("type", String, nullable=False),
    Column("geometry", JSONB, nullable=False),
    Column("properties", JSONB, nullable=False),
    Column("mapbox_uuid", String, nullable=True),
)
