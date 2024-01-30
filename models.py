from pydantic import BaseModel
from pydantic import Field


class Product(BaseModel):
    amount_available: int = Field(examples=[5])
    cost: int = Field(examples=[5, 10, 15, 20, 50, 100])
    product_name: str = Field(examples=['Cola'])
    seller_id: int = Field(examples=[2])


class User(BaseModel):
    username: str = Field(examples=['TylerDurden'])
    password: str = Field(examples=['Az195#?'])
    deposit: int = Field(examples=[50])
    role: str = Field(examples=['seller', 'buyer'])  # make another Model or Enum
