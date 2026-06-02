
from fastapi import FastAPI

from routes import router
from database import init_db
from log import get_logger


# Create FastAPI application instance
app = FastAPI(title="Address Book API")

# Create application logger
logger = get_logger(__name__)


# Startup event runs once when the application starts.
# Used to initialise database tables and other startup tasks.
@app.on_event("startup")
async def startup():
    logger.info("Starting up — initialising database")

    # Create database tables if they do not exist
    await init_db()

    logger.info("Database ready")


# Health check / root endpoint
# Can be used to verify that the API is running.
@app.get("/")
async def root():
    return {"message": "Address Book API is running"}


# Register all address-related routes.
# All endpoints in routes.py will be available under:
# /addresses/*
#
# Examples:
# POST   /addresses/
# GET    /addresses/
# GET    /addresses/{id}
# PATCH  /addresses/{id}
# DELETE /addresses/{id}
# GET    /addresses/nearby/search
app.include_router(
    router,
    prefix="/addresses",
    tags=["Addresses"]
)