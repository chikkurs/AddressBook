import logging

from fastapi import FastAPI

from database import init_db
from log import get_logger



app = FastAPI(title="Address Book API")
logger = get_logger(__name__)


@app.on_event("startup")
async def startup():
    logger.info("Starting up — initialising database")
    await init_db()
    logger.info("Database ready")


@app.get("/")
async def root():
    return {"message": "Address Book API is running"}
