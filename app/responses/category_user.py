from typing import Union
from datetime import datetime
from pydantic import EmailStr, BaseModel
from app.responses.base import BaseResponse


class CategoryUserResponse(BaseResponse):
    id: int
    name: str
   
    
    
