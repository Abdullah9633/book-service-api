from pydantic import BaseModel

class TagCreateModel(BaseModel):
   name: str 
   
class AddTagToBookModel(BaseModel):
   book_uid: str 
   
