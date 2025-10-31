from typing import Optional
from pydantic import BaseModel, ConfigDict

# ===============================================
#           User Category Schemas
# ===============================================

# Base schema with common attributes.
class UserCategoryBase(BaseModel):
    name: str

# Schema used for creating a new category via an API request.
class UserCategoryCreate(UserCategoryBase):
    pass

# Schema for updating a category. All fields are optional.
class UserCategoryUpdate(BaseModel):
    name: Optional[str] = None

# Schema for returning a category in an API response.
class UserCategoryResponse(UserCategoryBase):
    id: int
    
    # Use model_config in Pydantic v2 instead of class Config
    model_config = ConfigDict(from_attributes=True)


