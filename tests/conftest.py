from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from app.services import auth
from app.models import models

auth_handler = auth.Auth()


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {"email": "helo123@gmail.com", "password": "password123","first_name":"Moinoluwa",
    "last_name":"Ogunare","username":"Moin223","gender":"Male"}
    res = client.post("/users/users/signup", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123","first_name":"Moyinoluwa",
    "last_name":"Ogundare","username":"Moyin223","gender":"Male"}
    res = client.post("/users/users/signup", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return auth_handler.encode_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client



@pytest.fixture
def test_rentals(test_user, session, test_user2):
    rentals_data = [{
        "name": "string",
        "booking_time": "2022-10-12T21:21:54.960Z",
        "Room_number": 32,
        "owner_id": test_user['id']
    }, {
        "name": "string",
        "booking_time": "2024-10-12T21:21:54.960Z",
        "Room_number": 23,
        "owner_id": test_user['id']
    },
        {
        "name": "string",
        "booking_time": "2023-10-12T21:21:54.960Z",
        "Room_number": 1,
        "owner_id": test_user['id']
    }, {
        "name": "string",
        "booking_time": "2024-10-12T21:21:54.960Z",
        "Room_number": 34,
        "owner_id": test_user2['id']
    }]

    def create_rentals_model(rentals):
        return models.Reservations(**rentals)
    rentals_map = map(create_rentals_model, rentals_data)
    rentals = list(rentals_map)
    session.add_all(rentals)
    session.commit()
    rentals = session.query(models.Reservations).all()
    return rentals


@pytest.fixture
def test_users(client,session):
    users_data = [
         {"email": "hello123@gmail.com", "password": "password123","first_name":"Moyinoluwa",
    "last_name":"Ogundare","username":"Moyin223","gender":"Male"},
     {"email": "hell123@gmail.com", "password": "password123","first_name":"Myinoluwa",
    "last_name":"Ogndare","username":"Moyn223","gender":"Male"},
     {"email": "ello123@gmail.com", "password": "password123","first_name":"Moyiluwa",
    "last_name":"Ogunre","username":"Min223","gender":"Male"}]

    def create_user_model(user):
        return models.User(**user)
    users_map = map(create_user_model,users_data)
    users = list(users_map)
    session.add_all(users)
    session.commit()
    users= session.query(models.User).all()
    return users
