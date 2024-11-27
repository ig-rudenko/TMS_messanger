from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from ..settings import DATABASE_URL


engine = create_async_engine(url=DATABASE_URL, echo=True)

session_maker = async_sessionmaker(bind=engine)


async def get_session():
    async with session_maker() as session:  # Подключение с базой данных.
        try:
            yield session  # Получение сессии и ПАУЗА.
        except Exception:
            await session.rollback()
            raise
