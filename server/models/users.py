from pydantic import(
    BaseModel,
    EmailStr
)

class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    id: int
    
class UserDB(User):
    hashed_password: str    