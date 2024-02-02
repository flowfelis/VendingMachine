from typing import List

from pydantic import BaseModel
from pydantic import Field


class UserBase(BaseModel):
    """
    Base class for User
    """
    username: str = Field(examples=['TylerDurden'])
    deposit: int = Field(examples=[50])
    role: str = Field(examples=['seller', 'buyer'])


class UserCreate(UserBase):
    """
    For creating
    """
    password: str = Field(examples=['Az195#?'])


class User(UserBase):
    """
    For reading and returning
    """
    pass

    class Config:
        orm_mode = True


class BaseProduct(BaseModel):
    """
    Product schema for reading, returning and creating
    """
    amount_available: int = Field(examples=[5])
    cost: int = Field(examples=[5, 10, 15, 20, 50, 100])
    product_name: str = Field(examples=['Cola'])


class ProductCreate(BaseProduct):
    pass


class Product(BaseProduct):
    seller_id: int = Field(examples=[2])

    class Config:
        orm_mode = True


class Buy(BaseModel):
    """
    Schema for the buy endpoint
    """
    total_spent: int = Field(examples=[60])
    product_name: str = Field(examples=['Cola'])
    change: List = Field(examples=[50, 20, 5])
