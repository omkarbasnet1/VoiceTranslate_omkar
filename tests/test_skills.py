"""
Testing for sprint project 2 room booking
Author: Omkar Basnet

 3 testing: Test 1 for login and get token
            test 2 for get available rooms and check data
            test 3 for book a room, then same room same time should be failed.
"""
import pytest
from datetime import datetime, timedelta

# Import
from Room_booking_skills import (
    load_env,
    do_login,
    available_rooms,
    get_my_bookings,
    reserve_room,
    cancel_my_booking
)


# Fixture to load credentials
@pytest.fixture(scope="module")
def config():
    conf = load_env()
    if not conf:
        pytest.fail("cannot run .env missing")
    return conf


# Fixture to log in once and provide the token to all tests
@pytest.fixture(scope="module")
def auth_token(config):
    token = do_login(
        config["server_host"],
        config["user_email"],
        config["user_password"]
    )
    if not token:
        pytest.fail("login failed")
    return token


# Test 1 log in and get a valid token string
def test_login(auth_token):
    print("\n Check login is working")
    assert auth_token is not None
    assert isinstance(auth_token, str)
    assert len(auth_token) > 10
    print(f" got token, length = {len(auth_token)}")


# Test 2 for available rooms
def test_available_rooms(config, auth_token):
    print("\n Test 2: Get available rooms")
    rooms = available_rooms(config["server_host"], auth_token)
    # should come back a list
    assert isinstance(rooms, list)
    assert len(rooms) > 0

    # Check the data of the first room
    first_room = rooms[0]
    assert 'id' in first_room, "Missing id"
    if 'room_name' in first_room:
        assert 'room_name' in first_room
    else:
        assert 'name' in first_room, "Missing name"

    print(f" found {len(rooms)} room, first id = {first_room['id']}")


# Test 3 for booking  and duplicate booking should be blocked
def test_booking_room(config, auth_token):
    rooms = available_rooms(config["server_host"], auth_token)
    assert rooms and len(rooms) > 0
    target_room = rooms[0]['id']

    # for booking
    (datetime.now() + timedelta(days=7)).replace(hour=15, minute=0, second=0)
    time_str = "2027-08-09T10:00:00"
    print(f"Attempting to book Room{target_room} at {time_str}")

    # first booking room
    result = reserve_room(config["server_host"], auth_token, target_room, time_str, duration=15)
    assert result is not None, "First booking failed"
    print(" First booking successful")

    # second booking same room should get blocked
    print(" processing duplicate booking")
    duplicate = reserve_room(config["server_host"], auth_token, target_room, time_str, duration=15)
    assert duplicate is None, "Double booking failed"
    print("Duplicate booking  blocked")

    # cleanup
    my_bookings = get_my_bookings(config["server_host"], auth_token)
    if my_bookings:
        booking_id = my_bookings[-1]['id']
        cancel_book = cancel_my_booking(config["server_host"], auth_token, booking_id)
        assert cancel_book[0] is True, "cleanup failed"
        print(f" cleanup successful: cancelled Booking ID {booking_id}")
    else:
        print("Error: Could not find booking in list ")
