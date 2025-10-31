from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_session
from app.services import user_category as service
# CORRECTED: Import the schema classes directly from the app.schemas module.
from app.schemas import UserCategoryResponse, UserCategoryCreate, UserCategoryUpdate

category_router = APIRouter(
    prefix="/categories",
    tags=["User Categories"],
    responses={404: {"description": "Not found"}},
)

@category_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserCategoryResponse)
async def create_new_category(category: UserCategoryCreate, db: Session = Depends(get_session)):
    """
    Create a new user category.
    """
    return service.create_category(db, category)

@category_router.get("", response_model=List[UserCategoryResponse])
async def read_all_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    """
    Retrieve all user categories.
    """
    return service.get_all_categories(db, skip, limit)

@category_router.get("/{category_id}", response_model=UserCategoryResponse)
async def read_category_by_id(category_id: int, db: Session = Depends(get_session)):
    """
    Retrieve a single user category by its ID.
    """
    return service.get_category_by_id(db, category_id)

@category_router.put("/{category_id}", response_model=UserCategoryResponse)
async def update_existing_category(category_id: int, category: UserCategoryUpdate, db: Session = Depends(get_session)):
    """
    Update a user category.
    """
    return service.update_category(db, category_id, category)

@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_category(category_id: int, db: Session = Depends(get_session)):
    """
    Delete a user category. It cannot be deleted if in use.
    """
    service.delete_category(db, category_id)
    return None