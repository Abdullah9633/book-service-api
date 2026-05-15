from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from .schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.errors import BookNotFound
from sqlmodel import select, desc

user_service = UserService()
book_service = BookService()


class ReviewService:

    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        try:
            book = await book_service.get_book(session=session, book_uid=book_uid)

            if book is None:
                raise BookNotFound()

            user = await user_service.get_user_by_email(
                email=user_email, session=session
            )

            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)

            new_review.user = user
            new_review.book = book

            """
            print("\n\n\n\n\n\n\n")
            print(new_review.user)
            print("\n\n\n\n\n\n\n")
            print(new_review.book)
            print("\n\n\n\n\n\n\n")
            """

            session.add(new_review)
            await session.commit()
            return new_review

        except Exception as e:
            raise e


    async def get_all_reviews_on_book(self, session: AsyncSession, book_uid: str):
        my_statement = (
            select(Review)
            .where(Review.book_uid == book_uid)
            .order_by(Review.updated_at)
        )

        result = await session.exec(my_statement)
        return result.all()
    
    
    async def get_all_reviews_by_user(self, session: AsyncSession, user_uid: str):
        my_statement = (
            select(Review)
            .where(Review.user_uid == user_uid)
            .order_by(Review.updated_at)
        )

        result = await session.exec(my_statement)
        return result.all()


    async def get_review_by_id(self, session: AsyncSession, review_uid: str):
        my_statement = (
            select(Review)
            .where(Review.uid == review_uid)
        )

        result = await session.exec(my_statement)
        return result.first()


    async def delete_review_by_id(self, session: AsyncSession, review_uid: str):
        
        review_to_delete = await self.get_review_by_id(session, review_uid)

        if review_to_delete is not None:
            await session.delete(review_to_delete)
            await session.commit()
            return {}
        
        else:
            return None


