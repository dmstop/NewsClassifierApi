from logging_config import setup_logging
setup_logging()

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
import asyncio
from predictor import news_classifier
from db_model.database import init_db, drop_db
from db_model.repository import create_prediction, get_or_create_request_ip, delete_oldest_predictions

import logging

from timeit import default_timer as timer
from config import MAX_DB_LENGHT
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)   

@asynccontextmanager
async def app_lifespan(app: FastAPI):
     
    logger.info("Application startup")
    logger.info("Drop tables")
    await drop_db()
    logger.info("Init tables")
    await init_db()
    logger.info("Db ready")
    try:
        yield
    finally:
        logger.info("Application shutdown")

app = FastAPI(lifespan=app_lifespan)

class NewsText(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="The text of the news")

class PredictionResponse(BaseModel):
    label: str
    probability: float
    elapsed_time: float

@app.post("/NewsClassifier", response_model=PredictionResponse, tags=["Main"])
async def predict(request: Request, request_data: NewsText):
    
    client_ip = request.client.host

    start = timer()
    label, prob = await asyncio.to_thread(news_classifier.predict, request_data.text)
    end = timer()
    elapsed_time=round(end - start, 2)

    request_ip_id = await get_or_create_request_ip(client_ip)    
    await delete_oldest_predictions(max_rows=MAX_DB_LENGHT)
    prediction_id = await create_prediction(request_data.text, label, prob, elapsed_time, request_ip_id)
    
    return PredictionResponse(label=label, probability=round(prob, 2), elapsed_time=elapsed_time)