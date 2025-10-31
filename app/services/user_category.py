from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_category import UserCategory
# CORRECTED: Import the specific Pydantic classes you need.
from app.schemas.user_category import UserCategoryCreate, UserCategoryUpdate

# The rest of the file uses these classes directly
def create_category(db: Session, category: UserCategoryCreate):
    """
    Creates a new user category in the database.
    """
    existing_category = db.query(UserCategory).filter(UserCategory.name == category.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{category.name}' already exists."
        )
    db_category = UserCategory(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category_by_id(db: Session, category_id: int):
    """
    Fetches a single user category by its ID.
    """
    db_category = db.query(UserCategory).filter(UserCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found."
        )
    return db_category

def get_all_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches all user categories with pagination.
    """
    return db.query(UserCategory).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, category: UserCategoryUpdate):
    """
    Updates an existing user category.
    """
    db_category = get_category_by_id(db, category_id)
    if category.name and db.query(UserCategory).filter(UserCategory.name == category.name, UserCategory.id != category_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{category.name}' already exists."
        )
    update_data = category.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    """
    Deletes a user category.
    """
    db_category = get_category_by_id(db, category_id)
    if db_category.users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category. It is currently assigned to one or more users."
        )
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully."}