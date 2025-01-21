from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    Query,
    status
)

from typing import List, Tuple

from models.schemas import (
    PostCreate, 
    PostDB, 
    PostPartialUpdate,
    PostPublic,
    CommentDB,
)

from models.db_models import posts, comments
from database import get_database
from databases import Database

router = APIRouter()

async def get_post_or_404(
    id: int, database: Database = Depends(get_database)
) -> PostPublic:
    select_post_query = posts.select().where(posts.c.id == id)
    raw_post = await database.fetch_one(select_post_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    select_post_comments_query = comments.select().where(comments.c.post_id == id)
    raw_comments = await database.fetch_all(select_post_comments_query)
    comments_list = [CommentDB(**comment) for comment in raw_comments]

    return PostPublic(**raw_post, comments=comments_list)

async def pagination(skip: int= Query(0, ge=0), limit: int= Query(10,ge=0)) -> Tuple[int,int]:
    capped_limit= min(100, limit)
    
    return (skip, capped_limit)

@router.post('/posts', response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, database: Database= Depends(get_database)) -> PostDB:
    insert_query= posts.insert().values(post.model_dump())
    post_id= await database.execute(insert_query)
    post_db= await get_post_or_404(post_id, database)
    
    return post_db
    
@router.patch('/posts/{id}', response_model=PostDB)
async def update_post(post_update: PostPartialUpdate, post: PostDB= Depends(get_post_or_404), database: Database= Depends(get_database)) -> PostDB:
    update_query= posts.update().where(posts.c.id == post.id).values(post_update.model_dump(exclude_unset=True))
    await database.execute(update_query)
    post_db= await get_post_or_404(post.id, database)
    
    return post_db

@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post: PostDB = Depends(get_post_or_404), database: Database = Depends(get_database)):
    delete_query= posts.delete().where(post.c.id == post.id)
    await database.execute(delete_query)
    
@router.get('/posts')
async def list_posts(pagination: Tuple[int,int]= Depends(pagination), database: Database = Depends(get_database)) -> List[PostDB]:
    skip, limit= pagination
    select_query= posts.select().offset(skip).limit(limit)
    rows= await database.fetch_all(select_query)
    results= [PostDB(**row) for row in rows]
    
    return results

@router.get('/posts/{id}', response_model=PostDB)
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    return post