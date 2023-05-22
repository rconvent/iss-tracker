import logging

import requests
import sentry_sdk
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from src.config import app_configs, settings
from src.database import database
from src.iss.router import router as iss_router
from src.iss.schemas import ISSResponseIn
from src.iss.service import insert_iss_data
from starlette.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

app = FastAPI(**app_configs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )

@app.on_event("startup")
async def startup()-> None:
    await database.connect()

@app.on_event("startup")
@repeat_every(seconds=5, logger=logger, wait_first=True)  
async def retrieve_iss_data_task() -> None:
    logger.log(logging.INFO, "Retrieving ISS data")
    
    url = "https://api.wheretheiss.at/v1/satellites/25544"
    data = requests.request("GET", url).json()
     
    await insert_iss_data(ISSResponseIn(**data))

@app.on_event("shutdown")
async def shutdown() -> None:
    # Shutdown
    await database.disconnect()

@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(iss_router, prefix="/iss", tags=["ISS"])
