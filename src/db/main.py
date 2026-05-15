from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import my_config

my_engine = AsyncEngine(
    create_engine(
        url=my_config.my_dataBase_url,
        # echo=True
    )
)

async def myinit__db():
    async with my_engine.begin() as conn:
        # mystatement = text("SELECT 'Hello world';")
        # myresult = await conn.execute(mystatement)
        # print(myresult.all())

        # from src.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_the_session() -> AsyncSession:
    
    The_Session = sessionmaker(
        bind= my_engine,
        class_= AsyncSession,
        expire_on_commit= False 
    )

    async with The_Session() as my_session:
        yield my_session


