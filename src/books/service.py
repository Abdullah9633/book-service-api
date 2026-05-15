from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from .schemas import BookCreateModel, BookUpdateModel
from src.db.models import Book


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)
        return result.all()

    async def get_user_books(self, session: AsyncSession, user_uid):
        statement = (
            select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )

        result = await session.exec(statement)
        return result.all()

    async def get_book(self, session: AsyncSession, book_uid: str):
        statement = select(Book).where(Book.uid == book_uid)

        result = await session.exec(statement)
        the_book = result.first()
        return the_book if the_book is not None else None

    async def create_book(
        self, session: AsyncSession, book_data: BookCreateModel, user_uid
    ):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)

        new_book.published_date = datetime.strptime(
            book_data_dict["published_date"], "%Y-%m-%d"
        )
        new_book.user_uid = user_uid

        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(
        self, session: AsyncSession, book_uid: str, update_data: BookUpdateModel
    ):
        book_to_update = await self.get_book(session, book_uid)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump()

            # We need to convert, update_data['published_date'], into date
            published_date = update_data_dict.pop("published_date")
            book_to_update.published_date = datetime.strptime(
                published_date, "%Y-%m-%d"
            )


            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)

            await session.commit()
            return book_to_update
        else:
            return None

    async def delete_book(self, session: AsyncSession, book_uid: str):
        book_to_delete = await self.get_book(session, book_uid)

        if book_to_delete is not None:
            await session.delete(book_to_delete)

            await session.commit()
            return {}

        else:
            return None
