from sqlalchemy.orm import Session
from app import models
from app import schemas
from app.utils import hash_password


# User
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        deposit=user.deposit,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.User):
    db_user = get_user(db, user_id)

    db_user.username = user.username
    db_user.deposit = user.deposit
    db_user.role = user.role

    db.add(db_user)
    db.commit()
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()


# Product
def get_product(db: Session, user_id: int):
    return db.query(models.Product).filter(models.Product.id == user_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.Product):
    db_product = models.Product(
        amount_available=product.amount_available,
        cost=product.cost,
        product_name=product.product_name,
        seller_id=product.seller_id,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, user: schemas.Product):
    db_product = get_product(db, product_id)

    db_product.amount_available = user.amount_available
    db_product.cost = user.cost
    db_product.product_name = user.product_name
    db_product.seller_id = user.seller_id

    db.add(db_product)
    db.commit()
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    db.delete(db_product)
    db.commit()
