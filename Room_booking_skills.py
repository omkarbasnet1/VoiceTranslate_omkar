"""
Room Booking reserve for project 2
Author:Omkar Basnet
       Software Engineering course
       Graduate Student
This program helps to connect to the meeting room booking and lets you books rooms and show available rooms.
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv


# Configuration and Setup
def load_env():
    load_dotenv()
    env_secrets = {
        "server_host": os.getenv("SERVER_URL"),
        "user_email": os.getenv("USER_EMAIL"),
        "user_password": os.getenv("USER_PASSWORD")
    }
    if not env_secrets["server_host"] or not env_secrets["user_email"]:
        print("ERROR: Missing in .env file")
        return None
    return env_secrets


# HELPER to handle server
def helper_response(response, expected_code=200):
    if response.status_code == expected_code or response.status_code == 201:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


# For admin login
def do_login(server_host, email, password):
    base = server_host.rstrip("/")
    login_url = f"{base}/api/v1/member/login/"

    login_data = {
        "email": email,
        "password": password
    }
    try:
        response = requests.post(login_url, json=login_data)

        if response.status_code == 200:
            data = response.json()
            token = data.get("access")
            if not token and "token" in data:
                token = data["token"].get("access")
            if token:
                print("Login Successful")
                return token

        print(f"Login fail: {response.status_code}")
        print(f"Response: {response.text}")
        return None

    except Exception as e:
        print(f"Error trying to login: {e}")
        return None


# for checking the available rooms
def available_rooms(server_host, tokens):
    base = server_host.rstrip("/")
    url = f"{base}/api/v1/meeting-rooms/available/"
    headers = {"Authorization": f"Bearer {tokens}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error available room: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error getting rooms: {e}")
        return None


# For room book
def reserve_room(server_host, token, room_id, iso_time, duration=15):
    base = server_host.rstrip("/")
    url = f"{base}/api/v1/meeting-rooms/{room_id}/book/"
    headers = {"Authorization": f"Bearer {token}"}

    # Calculate and time based on duration (15 mins)
    date_time = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%S")
    end_time = date_time + timedelta(minutes=duration)

    # format times how the API wants them
    api_format = "%Y-%m-%d %I:%M %p"
    start_str = date_time.strftime(api_format)
    end_str = end_time.strftime(api_format)

    data = {
        "start_time": start_str,
        "end_time": end_str,
        "no_of_persons": 1
    }
    print(f" (sending booking request to: {server_host})")
    print(f" (with data: {data})")

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        print(f"Booking failed: {response.status_code}")
        return None


# Show all bookings from the account
def get_my_bookings(server_host, token):
    base = server_host.rstrip("/")
    url = f"{base}/api/v1/meeting-rooms/my-bookings/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            bookings = response.json()
            print(f" You have {len(bookings)} bookings(s)")
            return bookings
        else:
            print(f"Couldn't get bookings:{response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []


# Cancel Booking by its ID
def cancel_my_booking(server_host, token, booking_id):
    base = server_host.rstrip("/")
    url = f"{base}/api/v1/meeting-rooms/{booking_id}/cancel-booking/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.delete(url, headers=headers)

        # 204 no content is standard for delete success
        if response.status_code == 200 or response.status_code == 204:
            print(f"Cancelled booking{booking_id}")
            return True
        else:
            print(f"Couldn't cancel: {response.status_code}")
            print(f"Reason: {response.text}")
            return False

    except Exception as e:
        print(f"Error cancelling: {e}")
        return False


# main function execution
def main():
    print("Room Booking Service")
    # load Config
    config = load_env()
    if not config:
        return

    base = config["server_host"]

    # login check
    print("\n testing login")
    token = do_login(base, config["user_email"], config["user_password"])
    if not token:
        return

    # Check rooms
    print("\n Testing available rooms ")
    room = available_rooms(base, token)
    if room:
        print(f"Found {len(room)} room")

        # Grab the first room
        first_room = room[0]
        room_id = first_room['id']
        print(f" will use Room ID : {room_id}")
    else:
        print("No rooms available. Cannot booking")
        return

    # Book a room
    print("\n Testing Booking")
    tmrw = (datetime.now() + timedelta(days=2)).replace(hour=12, minute=0, second=0)
    time_str = tmrw.strftime("%Y-%m-%dT%H:%M:%S")
    print(f"Process to book room {room_id} at {time_str}")
    result = reserve_room(base, token, room_id, time_str)

    # try to get the booking id
    booking_id = None
    if result:
        print("Booking done")
        if 'id' in result:
            booking_id = result['id']
        elif 'booking' in result and 'id' in result['booking']:
            booking_id = result['booking']['id']
        print(f"New Booking ID is: {booking_id}")
    # Check Booking exists
    print("\n Testing Get my Booking")
    my_bookings = get_my_bookings(base, token)

    # if unable to find ID from the response, it will find it in the list
    if not booking_id and my_bookings:
        booking_id = my_bookings[-1]['id']
        print(f" (found Booking ID from list: {booking_id})")

    # Clean up (cancel)
    print("\n Testing Cancel Booking")
    if booking_id:
        cancel_my_booking(base, token, booking_id)
    else:
        print(" No booking ID found to cancel")


if __name__ == "__main__":
    main()
