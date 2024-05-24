from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.core.config        import settings

class DatabaseHelper:
    def __init__(
        self, 
        url:  str,
        echo: bool = False,
    ):
        self.engine = create_async_engine(
            url  = url, 
            echo = echo,
        )
        self.session = async_sessionmaker(
            bind             = self.engine, 
            autoflush        = False, 
            expire_on_commit = False,
        )
    
    async def dispose(self):
        await self.engine.dispose()

    async def get_db(self):
        async with self.session() as session:
            yield session

db_helper = DatabaseHelper(
    url  = settings.db_url,
    echo = settings.db_echo,
)