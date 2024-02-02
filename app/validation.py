from fastapi import HTTPException
from fastapi import status

from app import models


def is_deposited_right_amount(money: int):
    """
    Validate if right amount is deposited.
    """
    if money not in (5, 10, 20, 50, 100):
        raise HTTPException(
            status_code=400,
            detail='Please deposit only 5, 10, 20, 50 or 100 cent coins'
        )


def is_buyer(role: str):
    """
    Make sure the user is a buyer, if not raise an exception
    """
    if role != 'buyer':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only buyers can do this operation',
        )


def is_seller(role: str):
    """
    Make sure the user is a seller, if not raise an exception
    """
    if role != 'seller':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only sellers can do this operation',
        )


def product_exists(product: models.Product):
    """
    Validate for product existence
    """
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')


def enough_product(product: models.Product, buy_amount: int):
    """
    Validate for enough product amount while buying
    """
    if product.amount_available < buy_amount:
        raise HTTPException(status_code=400, detail='Not enough product')


def user_has_enough_money(
        user: models.User,
        total_cost: int,
):
    """
    Make sure user has enough money to buy what he wants
    """
    if user.deposit < total_cost:
        raise HTTPException(status_code=400, detail='User does not have enough money')
