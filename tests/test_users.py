import pytest
import jwt
from app.models import schemas

from app.config import settings



# def test_create_user(client):
#     res = client.post(
#         "/users/users/signup", json={"email": "hello123@gmail.com", "password": "password123","first_name":"Moyinoluwa","last_name":"Ogundare","username":"Moyin223","gender":"Male"})

#     new_user = schemas.UserOutput(**res.json())
#     assert new_user.email == "hello123@gmail.com"
#     assert new_user.username == "moyin223"
#     assert res.status_code == 201


# def test_login_user(test_user, client):
#     res = client.post(
#         "/users/users/login", data={"username": test_user['email'], "password": test_user['password']})
#     login_res = schemas.Token(**res.json())
#     payload = jwt.decode(login_res.access_token,
#                          settings.secret,algorithms=['HS256'])
#     id = payload.get("sub")
#     assert id == test_user['id']
#     assert login_res.token_type == "bearer"
#     assert res.status_code == 200


# @pytest.mark.parametrize("email, password, status_code", [
#     ('wrongemail@gmail.com', 'password123', 403),
#     ('sanjeev@gmail.com', 'wrongpassword', 403),
#     ('wrongemail@gmail.com', 'wrongpassword', 403),
#     (None, 'password123', 422),
#     ('sanjeev@gmail.com', None, 422)
# ])
# def test_incorrect_login(test_user, client, email, password, status_code):
#     res = client.post(
#         "users/users/login", data={"username": email, "password": password})

#     assert res.status_code == status_code

# def test_get_all_users(client, test_users):
#     res = client.get("/users/users/all")
#     def validate(user):
#         return schemas.UserOutput(**user)
#     users_map = map(validate, res.json())
#     users_list = list(users_map)

#     assert len(res.json()) == len(test_users)
#     assert res.status_code == 200



def test_get_one_user_not_exist_with_id(client,test_users):
    res = client.get(f"/users/users/88888")
    assert res.status_code == 403

def test_get_a_user_with_id(client, test_users):
    res = client.get(f"/users/users/{test_users[0].id}")
    user = schemas.UserOutput(**res.json())
    assert user.id == test_users[0].id
    assert user.username == test_users[0].username
    assert user.email == test_users[0].email
    assert res.status_code == 200


def test_get_a_user_with_email(client, test_users):
    res = client.post(f"/users/users/email?email={test_users[0].email}")
    user = schemas.UserOutput(**res.json())
    assert user.id == test_users[0].id
    assert user.username == test_users[0].username
    assert user.email == test_users[0].email 
    assert res.status_code == 200

def test_get_a_user_with_wrong_email(client ,test_users):
    res = client.post(f"/users/users/email?email=eradnugo@gmail.com")
    assert res.status_code == 403
    
def test_get_a_user_with_username(client, test_users):
    res = client.post(f"/users/users/username?username={test_users[0].username}")
    user = schemas.UserOutput(**res.json())
    assert user.id == test_users[0].id
    assert user.email == test_users[0].email
    assert res.status_code == 200

def test_get_a_user_with_wrong_email(client ,test_users):
    res = client.post(f"/users/users/username?username=eradnugo123")
    assert res.status_code == 403


def test_unauthorized_user_delete_user(client, test_user):
    res = client.delete(
        f"/users/users/delete")
    assert res.status_code == 401




def test_delete_post_non_exist(authorized_client, test_user):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404