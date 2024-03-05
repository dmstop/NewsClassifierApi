from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False)

async def init_db():
    from db_model.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db():
    from db_model.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)