from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.configuration import configuration

engine = create_async_engine(configuration.database_url, pool_size=10, max_overflow=20, pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_database() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
