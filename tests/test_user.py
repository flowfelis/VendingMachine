from app import crud
from app import models


def test_create_user(client, db):
    response = client.post(
        "/users/",
        json={
            "username": "deadpool",
            "password": "chimichangas4life",
            'deposit': 0,
            'role': 'buyer',
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {'username': 'deadpool', 'deposit': 0, 'role': 'buyer'}

    user = crud.get_user(db, 1)
    assert user.id == 1


def test_get_user(client, db):
    user = models.User(
        username='Ali',
        hashed_password='abc123',
        deposit=0,
        role='buyer',
    )
    db.add(user)
    db.commit()

    response = client.get('/users/1')

    assert response.status_code == 200
    assert response.json() == {'username': 'Ali', 'deposit': 0, 'role': 'buyer'}


def test_get_users(client, db):
    user1 = models.User(
        username='Ali',
        hashed_password='abc123',
        deposit=0,
        role='buyer',
    )
    db.add(user1)

    user2 = models.User(
        username='John',
        hashed_password='abc1234',
        deposit=10,
        role='seller',
    )
    db.add(user2)

    db.commit()

    response = client.get('/users')
    assert response.status_code == 200
    assert response.json() == [{'username': 'Ali', 'deposit': 0, 'role': 'buyer'},
                               {'username': 'John', 'deposit': 10, 'role': 'seller'}]


def test_update_user(client, db):
    user1 = models.User(
        username='Ali',
        hashed_password='abc123',
        deposit=0,
        role='buyer',
    )
    db.add(user1)

    db.commit()

    response = client.put(
        '/users/1',
        json={'username': 'Ali2', 'deposit': 1, 'role': 'seller'}
    )
    assert response.status_code == 200
    assert response.json() == {'username': 'Ali2', 'deposit': 1, 'role': 'seller'}


def test_delete_user(client, db):
    user1 = models.User(
        username='Ali',
        hashed_password='abc123',
        deposit=0,
        role='buyer',
    )
    db.add(user1)

    db.commit()

    response = client.delete('/users/1')
    assert response.status_code == 200

    db_user = crud.get_user(db, 1)
    assert db_user is None
