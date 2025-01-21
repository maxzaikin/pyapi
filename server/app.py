from fastapi import FastAPI

# Import DB API
from database import (
    get_database, 
    sqlalchemy_engine
)

# Import models
from models.db_models import (
    metadata
)

# Import routes

from routers import (
    posts, 
    comments,
    users    
)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    await get_database().connect()
    metadata.create_all(sqlalchemy_engine)
    yield
    await get_database().disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(users.router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)