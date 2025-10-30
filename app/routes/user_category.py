from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_session
from app.services import user_category as service
from app.schemas import user_category as schemas
# You will need a dependency to check if the current user is an admin
# from app.config.security import get_current_admin_user 

# Create the router
category_router = APIRouter(
    prefix="/categories",
    tags=["User Categories"],
    # dependencies=[Depends(get_current_admin_user)], # UNCOMMENT to protect all routes in this file
    responses={404: {"description": "Not found"}},
)

@category_router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCategoryResponse)
async def create_new_category(category: schemas.UserCategoryCreate, db: Session = Depends(get_session)):
    """
    Create a new user category. (Admin only)
    """
    return service.create_category(db, category)

@category_router.get("", response_model=List[schemas.UserCategoryResponse])
async def read_all_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    """
    Retrieve all user categories.
    """
    return service.get_all_categories(db, skip, limit)

@category_router.get("/{category_id}", response_model=schemas.UserCategoryResponse)
async def read_category_by_id(category_id: int, db: Session = Depends(get_session)):
    """
    Retrieve a single user category by its ID.
    """
    return service.get_category_by_id(db, category_id)

@category_router.put("/{category_id}", response_model=schemas.UserCategoryResponse)
async def update_existing_category(category_id: int, category: schemas.UserCategoryUpdate, db: Session = Depends(get_session)):
    """
    Update a user category. (Admin only)
    """
    return service.update_category(db, category_id, category)

@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_category(category_id: int, db: Session = Depends(get_session)):
    """
    Delete a user category. It cannot be deleted if in use. (Admin only)
    """
    service.delete_category(db, category_id)
    # A 204 response should not have a body, so we return None
    return None