from cgi import test
import pytest
from app.models import schemas,models
import json

def test_get_all_rentals(client, test_rentals):
    res = client.get("/reservations/reservations/all")

    def validate(rentals):
        return schemas.Reservations_Output(**rentals)
    rentals_map = map(validate, res.json())
    rentals_list = list(rentals_map)

    assert len(res.json()) == len(test_rentals)
    assert res.status_code == 200


def test_get_one_rentals_not_exist_with_id(client,test_rentals):
    res = client.get(f"/reservations/reservations/833")
    assert res.status_code == 403

def test_get_a_rentals_with_id(client, test_rentals):
    res = client.get(f"/reservations/reservations/{test_rentals[0].id}")
    rentals = schemas.Reservations_Output(**res.json())
    assert rentals.id == test_rentals[0].id
    assert rentals.name == test_rentals[0].name
    assert rentals.Room_number == test_rentals[0].Room_number
    assert res.status_code == 200

def test_get_a_rentals_with_room_number(client, test_rentals):
    res = client.get(f"/reservations/reservations/room/{test_rentals[0].Room_number}")
    rentals = schemas.Reservations_Output(**res.json())
    assert rentals.id == test_rentals[0].id
    assert rentals.name == test_rentals[0].name
    assert res.status_code == 200

def test_get_one_rentals_not_exist_with_(client,test_rentals):
    res = client.get(f"/reservations/reservations/room/33434")
    assert res.status_code == 403


# @pytest.mark.parametrize("name, booking_time, Room_number", [
#     ("string",2022-10-12T21:21:54.960Z,32),
#     ("string",2023-10-12T21:21:54.960Z,2),
#     ("string",2023-10-12T21:21:54.960Z,22),
# ])
# def test_create_rentals(client, test_user,test_rentals,token):
#     data = {"name": "name", "booking_time": "2022-10-12T21:21:54.960Z", "Room_number": 23,"owner_id":test_user['id']}
#     # new_data = models.Reservations(**data)
#     newer_data = list(data)
#     res = client.post(
#         "/reservations/reservations/new_reservations",headers={ 'Authorization': f'Bearer {token}' },json=data)

#     created_rentals = schemas.Reservations(**res.json())
#     assert res.status_code == 201
#     assert created_rentals.Room_number == 23
#     assert created_rentals.booking_time == "2022-10-12T21:21:54.960Z"
#     assert created_rentals.name =="name"
# #     # assert created_rentals.owner_id == test_user['id']

def test_unauthorized_user_create_rentals(client, test_user, test_rentals):
    res = client.post(
        "/reservations/reservations/new_reservations", json={"name": "arbitrary title", "Room_number":32})
    assert res.status_code == 401
