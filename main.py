import logging

from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Address Book API")


@app.get("/")
async def root():
    return {"message": "Address Book API is running"}
