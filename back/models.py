from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from database import Base

class LoginRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    role: str




class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    category = Column(String)
    price = Column(Float)
    current_stock = Column(Integer)


class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    quantity = Column(Integer)
    total_price = Column(Float)
