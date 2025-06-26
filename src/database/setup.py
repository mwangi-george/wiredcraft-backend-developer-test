

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from ..config import env_vars

# configure the engine to connect to the database using the connection string
engine: AsyncEngine = create_async_engine(
    url=env_vars.db_url,
    future=True,
    connect_args={"statement_cache_size": 0},
    pool_pre_ping=True,  # ping the database before using a connection.
)

# create a session local factory bound to the engine
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

# function to yield the session - will be used in routes as a dependency
async def get_db():
    """ Async database session factory """
    async with SessionLocal() as session:
        yield session

