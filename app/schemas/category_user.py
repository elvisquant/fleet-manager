from typing import Optional
from pydantic import BaseModel

# Base schema with common attributes
class UserCategoryBase(BaseModel):
    name: str

# Schema for creating a new category (receives data from a request)
class UserCategoryCreate(UserCategoryBase):
    pass

# Schema for updating a category (all fields are optional)
class UserCategoryUpdate(BaseModel):
    name: Optional[str] = None

# Schema for reading/returning a category (includes the database ID)
class UserCategoryResponse(UserCategoryBase):
    id: int

    class Config:
        # This allows Pydantic to read data from ORM models
        from_orm = True