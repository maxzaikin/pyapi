from typing import (    
    cast,
    Mapping
)

from models.comments import (
    CommentCreate, 
    CommentDB
)
from database import get_database
from databases import Database

from models import (
    comments,
    posts
)

from fastapi import(
    APIRouter,
    Depends,
    HTTPException,
    status    
)

router = APIRouter()

@router.post("/comments", response_model=CommentDB, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: CommentCreate, database: Database = Depends(get_database)
) -> CommentDB:
    select_post_query = posts.select().where(posts.c.id == comment.post_id)
    post = await database.fetch_one(select_post_query)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post {comment.post_id} does not exist",
        )

    insert_query = comments.insert().values(comment.model_dump())
    comment_id = await database.execute(insert_query)

    select_query = comments.select().where(comments.c.id == comment_id)
    raw_comment = cast(Mapping, await database.fetch_one(select_query))

    return CommentDB(**raw_comment)
