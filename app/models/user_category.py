from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserCategory(Base):
    __tablename__ = 'user_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # This relationship allows me to find all users in a category
    users = relationship("User", back_populates="category")


