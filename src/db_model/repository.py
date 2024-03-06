from sqlalchemy.future import select
from sqlalchemy import func
from db_model.models import RequestIP, Prediction
from db_model.database import AsyncSessionLocal

async def create_prediction(text: str,
                            label: str,
                            probability: float,
                            elapsed_time: float, 
                            request_ip_id: int) -> int:
    
    async with AsyncSessionLocal() as db_session:
        prediction = Prediction(
            text=text,
            pred_label=label,
            probability=probability,
            elapsed_time=elapsed_time,
            request_ip_id=request_ip_id
        )

        db_session.add(prediction)
        await db_session.flush()
        await db_session.commit()
        await db_session.refresh(prediction)
        return prediction.id

async def get_or_create_request_ip(ip_address: str) -> int:
    async with AsyncSessionLocal() as db_session:
        result = await db_session.execute(select(RequestIP).filter_by(ip=ip_address))
        request_ip = result.scalars().first()

        if not request_ip:
            request_ip = RequestIP(ip=ip_address)
            db_session.add(request_ip)
            await db_session.flush()
            await db_session.commit()
            await db_session.refresh(request_ip)
        
        return request_ip.id

async def delete_oldest_predictions(max_rows: int = 10000):
    async with AsyncSessionLocal() as db_session:
        count_result = await db_session.execute(select(func.count(Prediction.id)))
        total_rows = count_result.scalar_one()

        if total_rows > max_rows:
            excess = total_rows - max_rows
            oldest_predictions_result = await db_session.execute(
                select(Prediction).order_by(Prediction.id).limit(excess)
            )
            oldest_predictions = oldest_predictions_result.scalars().all()
            for prediction in oldest_predictions:
                await db_session.delete(prediction)
            await db_session.commit()