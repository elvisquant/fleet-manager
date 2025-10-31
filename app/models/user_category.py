from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserCategory(Base):
    """
    SQLAlchemy model for the 'user_categories' table.
    """
    __tablename__ = 'user_categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # Establishes a one-to-many relationship with the User model.
    # 'back_populates' creates a link back from the User model to this one.
    users = relationship("User", back_populates="category")