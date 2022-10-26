from pydantic import BaseModel, EmailStr

# there are a schema used for user's endpoints


class UserBase(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserCreate(UserBase):
    pass


class User(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    pass
