from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)
    deposit = Column(Integer)
    role = Column(String)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    amount_available = Column(Integer)
    cost = Column(Integer)
    product_name = Column(String)
    seller_id = Column(Integer, ForeignKey('user.id'))

    seller = relationship('User', back_populates='product')
