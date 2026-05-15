from typing import List
from fastapi.exceptions import HTTPException
from fastapi import status

from .schemas import Book, BookUpdateModel, BookCreateModel, BookDetailModel
from src.db.main import get_the_session
from .service import BookService

book_service = BookService()

from fastapi import APIRouter

book_router = APIRouter()
from fastapi import Depends  # To use Dependcy Injection
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import MyAccessTokenBearer, RoleChecker
from src.errors import BookNotFound

access_token_bearer = MyAccessTokenBearer()
role_checker = RoleChecker(["admin", "user"])
admin_role_checker = RoleChecker(["admin"])


# Reading
@book_router.get("/", response_model=List[Book], dependencies=[Depends(role_checker)])
async def get_all_books(
    session: AsyncSession = Depends(get_the_session),
    token_details=Depends(access_token_bearer),
):
    print(token_details)
    books = await book_service.get_all_books(session)
    return books


@book_router.get(
    "/user/{user_uid}", response_model=List[Book], dependencies=[Depends(role_checker)]
)
async def get_user_books_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_the_session),
    token_details=Depends(access_token_bearer),
):

    books = await book_service.get_user_books(session, user_uid)
    return books


@book_router.get(
    "/{book_uid}", response_model=BookDetailModel, dependencies=[Depends(role_checker)]
)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_the_session),
    token_details=Depends(access_token_bearer),
) -> dict:

    book = await book_service.get_book(session, book_uid)

    if book:
        return book
    else:
        raise BookNotFound()


# Creating
@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    dependencies=[Depends(role_checker)],
)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_the_session),
    token_details=Depends(access_token_bearer),
) -> dict:

    user_uid = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(session, book_data, user_uid)
    return new_book


# Updating
@book_router.patch(
    "/{book_uid}", response_model=Book, dependencies=[Depends(role_checker)]
)
async def update_a_book(
    book_uid: str,
    update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_the_session),
    token_details=Depends(access_token_bearer),
) -> dict:

    updated_book = await book_service.update_book(session, book_uid, update_data)

    if updated_book:
        return updated_book
    else:
        raise BookNotFound()
    

# Deleting
@book_router.delete("/{book_uid}", dependencies=[Depends(admin_role_checker)])
async def delete_a_book(
    book_uid: str,
    session: AsyncSession = Depends(get_the_session),
    token_details=Depends(access_token_bearer),
):

    book_to_delete = await book_service.delete_book(session, book_uid)

    if book_to_delete is None:
        raise BookNotFound()
    else:
        return ["Book Deleted Successfully", "Thanks"]
