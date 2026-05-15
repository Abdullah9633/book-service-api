from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from .schemas import ReviewCreateModel
from .service import ReviewService
from src.db.main import get_the_session
from src.db.models import User
from src.auth.dependencies import get_current_user, RoleChecker
from sqlmodel.ext.asyncio.session import AsyncSession
from src.errors import ReviewNotFound

reviews_router = APIRouter()
review_service = ReviewService()
role_checker = RoleChecker(["user", "admin"])


@reviews_router.post("/book/{book_uid}")
async def add_review_to_books(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_the_session),
):
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        book_uid=book_uid,
        session=session,
        review_data=review_data,
    )

    return new_review
    

@reviews_router.get("/book/{book_uid}", dependencies= [Depends(role_checker)])
async def get_all_reviews_on_book(
    book_uid: str,
    session: AsyncSession = Depends(get_the_session)
):
    reviews = await review_service.get_all_reviews_on_book(
        session= session,
        book_uid= book_uid
    )
    
    return reviews
    
    
@reviews_router.get("/user/{user_uid}", dependencies= [Depends(role_checker)])
async def get_all_reviews_by_user(
    user_uid: str,
    session: AsyncSession = Depends(get_the_session)
):
    reviews = await review_service.get_all_reviews_by_user(
        session= session,
        user_uid= user_uid
    )
    
    return reviews
    
    
@reviews_router.get("/{review_uid}", dependencies= [Depends(role_checker)])
async def get_review_by_uid(
    review_uid: str,
    session: AsyncSession = Depends(get_the_session)
):
    review = await review_service.get_review_by_id(
        session= session,
        review_uid= review_uid
    )
    
    return review
    
    
@reviews_router.delete("/{review_uid}", dependencies= [Depends(role_checker)])
async def delete_review_by_id(
    review_uid: str,
    session: AsyncSession = Depends(get_the_session)
):
    delete_review = await review_service.delete_review_by_id(session, review_uid)
    
    if delete_review is None:
        raise ReviewNotFound()
    
    return JSONResponse(
        content= {
            "message": "Review deleted successfully!"
        },
        status_code= status.HTTP_200_OK
    )


