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



def test_unauthorized_user_create_rentals(client, test_user, test_rentals):
    res = client.post(
        "/reservations/reservations/new_reservations", json={"name": "arbitrary title", "Room_number":32})
    assert res.status_code == 401