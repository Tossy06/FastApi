from sqlalchemy import Column, Integer,Float, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, index= True)
    email = Column(String, unique=True, index=True, nullable= False)
    password_hash = Column(String, nullable= False)
    role = Column(String, default="user")
    active = Column(Boolean, default= True)
    notes = relationship("Note", back_populates="owner")

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key= True, index= True)
    title= Column(String, nullable= False)
    content = Column(String, nullable= False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable= False)
    owner    = relationship("User", back_populates="notes")

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    price = Column(Float, nullable = False)
    stock = Column(Integer, default = 0)
    category = Column(String, nullable = True)