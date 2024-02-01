from typing import List

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app import crud
from app import models
from app import schemas
from app.database import engine
from app.database import get_db
from app.security import authenticate
from app import validation

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# User
@app.get('/users/', response_model=List[schemas.User])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        _=Depends(authenticate)
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(
        user_id: int,
        db: Session = Depends(get_db),
        _=Depends(authenticate),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.post('/users/', response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='User already exists')
    return crud.create_user(db=db, user=user)


@app.put('/users/{user_id}', response_model=schemas.User)
def update_user(
        user_id: int,
        user: schemas.User,
        db: Session = Depends(get_db),
        _=Depends(authenticate),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return crud.update_user(db, user_id, user)


@app.delete('/users/{user_id}', response_model=schemas.User)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        _=Depends(authenticate),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    db.delete(db_user)
    db.commit()
    return db_user


# Product
@app.get('/products/', response_model=List[schemas.Product])
def read_products(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.get('/products/{product_id}', response_model=schemas.Product)
def read_product(
        product_id: int,
        db: Session = Depends(get_db),
):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return db_product


@app.post('/products/', response_model=schemas.Product)
def create_product(
        product: schemas.Product,
        db: Session = Depends(get_db),
        logged_in_user_id: int = Depends(authenticate),
):
    if product.seller_id != logged_in_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only the seller who created the product is allowed',
        )
    db_product = crud.get_product_by_name(db, product_name=product.product_name)
    if db_product:
        raise HTTPException(status_code=400, detail='Product already exists')
    return crud.create_product(db=db, product=product)


@app.put('/products/{product_id}', response_model=schemas.Product)
def update_product(
        product_id: int,
        product: schemas.Product,
        db: Session = Depends(get_db),
        logged_in_user_id: int = Depends(authenticate)
):
    if product.seller_id != logged_in_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only the seller who created the product is allowed',
        )
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return crud.update_product(db, product_id, product)


@app.delete('/products/{product_id}', response_model=schemas.Product)
def delete_product(
        product_id: int,
        db: Session = Depends(get_db),
        logged_in_user_id: int = Depends(authenticate),
):
    db_product = crud.get_product(db, product_id)
    if db_product.seller_id != logged_in_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only the seller who created the product is allowed',
        )
    validation.product_exists(db_product)

    db.delete(db_product)
    db.commit()
    return db_product


@app.put('/deposit/{money}', response_model=schemas.User)
def deposit(
        money: int,
        db: Session = Depends(get_db),
        logged_in_user_id=Depends(authenticate),
):
    # make sure user is a buyer
    db_user = crud.get_user(db, logged_in_user_id)
    validation.is_buyer(db_user.role)

    # make sure right amount is deposited
    validation.is_deposited_right_amount(money)

    # update user's deposit
    db_user.deposit += money
    crud.update_user(db, db_user.id, db_user)

    return db_user


@app.put('/buy/{product_id}/{amount}', response_model=schemas.Buy)
def buy(
        product_id: int,
        buy_amount: int,
        db: Session = Depends(get_db),
        logged_in_user_id=Depends(authenticate),
):
    db_user = crud.get_user(db, logged_in_user_id)
    db_product = crud.get_product(db, product_id)

    validation.is_buyer(db_user.role)
    validation.product_exists(db_product)
    validation.enough_product(db_product, buy_amount)

    total_cost = db_product.cost * buy_amount
    validation.user_has_enough_money(db_user, total_cost)

    change = db_user.deposit - total_cost

    db_product.amount_available -= buy_amount
    crud.update_product(db, product_id, db_product)

    db_user.deposit -= total_cost
    crud.update_user(db, db_user.id, db_user)

    return schemas.Buy(
        total_spent=total_cost,
        product_name=db_product.product_name,
        change=change,
    )


@app.put('/reset', response_model=schemas.User)
def reset(
        db: Session = Depends(get_db),
        logged_in_user_id=Depends(authenticate),
):
    db_user = crud.get_user(db, logged_in_user_id)
    if db_user.deposit == 0:
        raise HTTPException(status_code=400, detail='Deposit is already 0')

    db_user.deposit = 0
    crud.update_user(db, db_user.id, db_user)

    return db_user
