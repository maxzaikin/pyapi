from typing import(
    Optional,
    List
)

from pydantic import (
    BaseModel, 
    Field
)

from datetime import datetime
from typing import Optional
from models.comments import CommentDB

class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

class PostDB(PostBase):
    id: int

class PostPublic(PostDB):
    comments: List[CommentDB]
    
class PostCreate(PostBase):
    pass

class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    
