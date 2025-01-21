from pydantic import (
    BaseModel, 
    Field
)

from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    post_id: int
    publication_date: datetime = Field(default_factory=datetime.now)
    content: str

class CommentCreate(CommentBase):
    pass

class CommentDB(CommentBase):
    id: int