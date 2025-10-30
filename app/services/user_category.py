from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_category import UserCategory
from app.schemas import user_category as schemas

def create_category(db: Session, category: schemas.UserCategoryCreate):
    """
    Creates a new user category in the database.
    Checks if a category with the same name already exists.
    """
    # Check for duplicates
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
    Raises a 404 error if not found.
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

def update_category(db: Session, category_id: int, category: schemas.UserCategoryUpdate):
    """
    Updates an existing user category.
    """
    db_category = get_category_by_id(db, category_id) # Reuse get_category_by_id to handle 404
    
    # Check if the new name is already taken by another category
    if category.name and db.query(UserCategory).filter(UserCategory.name == category.name, UserCategory.id != category_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{category.name}' already exists."
        )

    # Get update data, excluding fields that were not sent
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
    Prevents deletion if any users are currently assigned to this category.
    """
    db_category = get_category_by_id(db, category_id)
    
    # IMPORTANT: Check if any users are using this category before deleting
    if db_category.users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category. It is currently assigned to one or more users."
        )
        
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully."}