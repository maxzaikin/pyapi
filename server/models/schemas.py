from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class CommentBase(BaseModel):
    post_id: int
    publication_date: datetime = Field(default_factory=datetime.now)
    content: str

class CommentCreate(CommentBase):
    pass

class CommentDB(CommentBase):
    id: int

class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostDB(PostBase):
    id: int

class PostPublic(PostDB):
    comments: List[CommentDB]
