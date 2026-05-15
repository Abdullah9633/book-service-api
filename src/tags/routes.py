from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import RoleChecker
from src.db.main import get_the_session
from .schemas import TagCreateModel, AddTagToBookModel
from .service import TagsService

tags_router = APIRouter()
role_checker = RoleChecker(["admin"])
tags_service = TagsService()


@tags_router.get("/", dependencies=[Depends(role_checker)])
async def get_all_tags(session: AsyncSession = Depends(get_the_session)):

    result = await tags_service.get_all_tags(session)
    return result


@tags_router.get("/{tag_uid}", dependencies=[Depends(role_checker)])
async def get_tag_by_its_uid(tag_uid, session: AsyncSession = Depends(get_the_session)):

    result = await tags_service.get_tag_by_its_uid(session=session, tag_uid=tag_uid)
    return result


@tags_router.post("/", dependencies=[Depends(role_checker)])
async def create_tag(
    tag_data: TagCreateModel, session: AsyncSession = Depends(get_the_session)
):

    result = await tags_service.create_tag(session=session, tag_data=tag_data)

    return result


@tags_router.put("/{tag_uid}", dependencies=[Depends(role_checker)])
async def update_tag(
    tag_uid: str,
    tag_data: TagCreateModel,
    session: AsyncSession = Depends(get_the_session),
):

    result = await tags_service.update_tag(
        session=session, tag_data=tag_data, tag_uid=tag_uid
    )

    return result


@tags_router.delete("/{tag_uid}", dependencies=[Depends(role_checker)])
async def delete_tag(
    tag_uid: str,
    session: AsyncSession = Depends(get_the_session),
):

    result = await tags_service.delete_tag(session=session, tag_uid=tag_uid)

    return JSONResponse(
        content={"message": "Tag deleted Successfully!"}, status_code=status.HTTP_200_OK
    )


@tags_router.post("/book/{tag_uid}", dependencies=[Depends(role_checker)])
async def add_tag_to_book(
    tag_uid: str,
    book_data: AddTagToBookModel,
    session: AsyncSession = Depends(get_the_session),
):

    book_uid = book_data.book_uid
    result = await tags_service.add_tag_to_book(
        session=session, book_uid=book_uid, tag_uid=tag_uid
    )

    return JSONResponse(
        content={"message": "Tag added to the book Successfully!"}, status_code=status.HTTP_200_OK
    )
    
    
@tags_router.delete("/book/{tag_uid}", dependencies=[Depends(role_checker)])
async def remove_tag_from_book(
    tag_uid: str,
    book_data: AddTagToBookModel,
    session: AsyncSession = Depends(get_the_session),
):

    book_uid = book_data.book_uid
    result = await tags_service.remove_tag_from_book(
        session=session, book_uid=book_uid, tag_uid=tag_uid
    )

    return JSONResponse(
        content={"message": f"Tag {tag_uid} removed from the book {book_uid} Successfully!"}, status_code=status.HTTP_200_OK
    )
    
    
@tags_router.get("/book/{book_uid}", dependencies=[Depends(role_checker)])
async def get_all_tags_of_book(
    book_uid: str,
    session: AsyncSession = Depends(get_the_session),
):

    result = await tags_service.get_all_tags_of_book(
        session=session, book_uid=book_uid
    )

    return result
    
    
@tags_router.get("/booktag/{tag_uid}", dependencies=[Depends(role_checker)])
async def get_all_books_of_tag(
    tag_uid: str,
    session: AsyncSession = Depends(get_the_session),
):

    result = await tags_service.get_all_books_of_tag(
        session=session, tag_uid=tag_uid
    )

    return result



