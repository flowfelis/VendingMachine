import pytest

from app import crud
from app import models


@pytest.mark.parametrize('money', [5, 10, 20, 50])
def test_deposit_success(client, db, money):
    user = models.User(
        username='Ali',
        hashed_password='abc123',
        deposit=0,
        role='buyer',
    )
    db.add(user)
    db.commit()

    response = client.post(f'/deposit/{money}')
    assert response.status_code == 200
    assert response.json() == {'username': 'Ali', 'deposit': money, 'role': 'buyer'}

    db_user = crud.get_user(db, user.id)
    assert db_user.deposit == money


def test_deposit_fail_wrong_money(client, db):
    user = models.User(
        username='Ali',
        hashed_password='abc123',
        deposit=0,
        role='buyer',
    )
    db.add(user)
    db.commit()

    response = client.post(f'/deposit/3')
    assert response.status_code == 400


def test_deposit_fail_wrong_role(client, db):
    user = models.User(
        username='Ali',
        hashed_password='abc123',
        deposit=0,
        role='seller',
    )
    db.add(user)
    db.commit()

    response = client.post(f'/deposit/3')
    assert response.status_code == 403


def test_buy_success(client, db):
    user = models.User(
        username='Ali',
        hashed_password='abc123',
        deposit=40,
        role='buyer',
    )
    db.add(user)

    product = models.Product(
        amount_available=4,
        cost=20,
        product_name='Chips',
        seller_id=1,
    )
    db.add(product)
    db.commit()

    response = client.post('/buy/1/2')
    assert response.status_code == 200
    assert response.json() == {'total_spent': 40, 'product_name': 'Chips', 'change': []}

    # user should have 0 deposit
    db_user = crud.get_user(db, 1)
    assert db_user.deposit == 0

    # product amount available should be 2
    db_product = crud.get_product(db, 1)
    assert db_product.amount_available == 2


def test_buy_fail_user_dont_have_enough_money(client, db):
    user = models.User(
        username='Ali',
        hashed_password='abc123',
        deposit=40,
        role='buyer',
    )
    db.add(user)

    product = models.Product(
        amount_available=4,
        cost=20,
        product_name='Chips',
        seller_id=1,
    )
    db.add(product)
    db.commit()

    response = client.post('/buy/1/3')
    assert response.status_code == 400
    assert response.json() == {'detail': 'User does not have enough money'}
