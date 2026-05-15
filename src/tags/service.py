from src.books.service import BookService
from src.db.models import Tag, Book
from sqlmodel.ext.asyncio.session import AsyncSession
from src.errors import TagAlreadyExists, TagNotFound, BookNotFound, TagAlreadyOnBook, TagNotOnBook
from sqlmodel import select
from .schemas import TagCreateModel
from src.books.service import BookService
from datetime import datetime

book_servive = BookService()


class TagsService:
    
    async def get_all_tags(self, session: AsyncSession):
        statement = select(Tag).order_by(Tag.updated_at)
        
        result = await session.exec(statement= statement)
        
        return result.all()
    
    
    async def get_tag_by_its_uid(self, session: AsyncSession, tag_uid: str):
        statement = select(Tag).where(Tag.uid == tag_uid)
        
        result = await session.exec(statement= statement)
        
        result = result.first()
        
        if result is None:
            raise TagNotFound()

        return result
    
    
    async def create_tag(self, session: AsyncSession, tag_data: TagCreateModel):
        name = tag_data.name
        
        statement = select(Tag).where(Tag.name == name)
        result = await session.exec(statement= statement)
        
        result = result.first()
        
        if result is not None:
            raise TagAlreadyExists()
        
        tag_dta_dict = tag_data.model_dump()
        
        new_tag = Tag(**tag_dta_dict)
        
        session.add(new_tag)
        await session.commit()
        
        return new_tag
    
    
    async def update_tag(self, session: AsyncSession, tag_data: TagCreateModel, tag_uid: str):        
        tag_to_update = await self.get_tag_by_its_uid(session= session, tag_uid= tag_uid)
        
        tag_dta_dict = tag_data.model_dump()
        
        for k, v in tag_dta_dict.items():
            setattr(tag_to_update, k, v)
            
        tag_to_update.updated_at = datetime.now()
        
        await session.commit()
        return tag_to_update
        
    
    async def delete_tag(self, session: AsyncSession, tag_uid: str):        
        tag_to_delete = await self.get_tag_by_its_uid(session= session, tag_uid= tag_uid)
        
        await session.delete(tag_to_delete)
        
        await session.commit()
        return {}
        
    
    async def add_tag_to_book(self, session: AsyncSession, tag_uid: str, book_uid: str):        
        book_to_update = await book_servive.get_book(session= session, book_uid= book_uid)
        
        if book_to_update is None:
            raise BookNotFound()

        tag_to_add = await self.get_tag_by_its_uid(session= session, tag_uid= tag_uid)
        
        if tag_to_add is None:
            raise TagNotFound()
        
        if tag_to_add in book_to_update.tags:
            raise TagAlreadyOnBook()
        
        book_to_update.tags.append(tag_to_add)
        
        await session.commit()
        return {}
    
    
    async def remove_tag_from_book(self, session: AsyncSession, tag_uid: str, book_uid: str):        
        book_to_update = await book_servive.get_book(session= session, book_uid= book_uid)
        
        if book_to_update is None:
            raise BookNotFound()

        tag_to_remove = await self.get_tag_by_its_uid(session= session, tag_uid= tag_uid)
        
        if tag_to_remove is None:
            raise TagNotFound()
        
        if tag_to_remove not in book_to_update.tags:
            raise TagNotOnBook()
            
        book_to_update.tags.remove(tag_to_remove) 
        await session.commit()
        return {}
    
    
    async def get_all_books_of_tag(self, session: AsyncSession, tag_uid: str):        
        the_tag = await self.get_tag_by_its_uid(session= session, tag_uid= tag_uid)
        
        if the_tag is None:
            raise TagNotFound()
            
        statement = select(Book).where(Book.tags.contains(the_tag))

        result = await session.exec(statement= statement)

        return result.all()
    
    
    async def get_all_tags_of_book(self, session: AsyncSession, book_uid: str):        
        the_book = await book_servive.get_book(session= session, book_uid = book_uid)
        
        if the_book is None:
            raise BookNotFound()
        
        return the_book.tags
    

