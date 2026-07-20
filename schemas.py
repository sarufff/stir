from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    name: str | None
    email: str
    subscription_type: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class PantryItemCreate(BaseModel):
    name: str

class PantryItemOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True