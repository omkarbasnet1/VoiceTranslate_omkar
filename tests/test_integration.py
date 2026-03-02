"""
    Integration test for Sprint 3

    Tests the whole end to end
    voice file - whisper - AI agent - check response
"""
import os
import pytest
import whisper

from Room_booking_skills import (
    load_env,
    do_login,
    available_rooms,
    reserve_room,
    get_my_bookings,
    cancel_my_booking,
)

from ai_agent import (
    setup_agent,
    ask_agent
)

from main import audio_transcription


# loads ( whisper model, langchain agent, config)
@pytest.fixture(scope="module")
def setup_data():
    config = load_env()
    if not config:
        pytest.fail("missing .env file")

    host = config["server_host"]
    token = do_login(config["server_host"], config["user_email"], config["user_password"])
    agent = setup_agent()
    model = whisper.load_model("base")

    return host, token, agent, model


# integration test of voice AI
def test_end_agent(setup_data):
    host, token, agent, whisper_model = setup_data

    # Reserve a meeting room
    print("For reservation.")
    rooms = available_rooms(host, token)
    assert rooms and len(rooms) > 0, "No rooms available"

    target_room_id = rooms[0]['id']
    time_str = "2027-05-08T10:00:00"

    booking_result = reserve_room(host, token, target_room_id, time_str, duration=15)
    assert booking_result is not None, "Failed to book room"

    # Booking ID for the cleanup
    booking_id = None
    if 'id' in booking_result:
        booking_id = booking_result['id']
    elif 'booking' in booking_result and 'id' in booking_result['booking']:
        booking_id = booking_result['booking']['id']

    print(f" Booked room success {target_room_id}")
    print(f"Booking ID: {booking_id}")

    print(" Reading voice file...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    audio_file = os.path.join(current_dir, "test_audio.wav")
    if not os.path.exists(audio_file):
        pytest.fail(f"Missing : {audio_file}")

    transcribed_text = audio_transcription(whisper_model, audio_file)
    assert len(transcribed_text) > 0, "return empty string"
    print(f" Transcribed: {transcribed_text}")

    print(" Sending  to the AI agent...")
    ai_response = ask_agent(agent, transcribed_text)
    print(f" AI answer: {ai_response}")

    assert len(ai_response) > 0, "AI will not answer"
    assert "Error" not in ai_response, "Error in AI"

    # Remove the reservation
    print("\n Cleaning up reservation")
    my_bookings = get_my_bookings(host, token)
    if my_bookings and len(my_bookings) > 0:
        booking_id = my_bookings[-1]['id']
        print(f"Found booking id :{booking_id}.. Cancelling..")
        cancel_success = cancel_my_booking(host, token, booking_id)
        assert cancel_success is True, "failed to remove"
    else:
        pytest.fail("don not find booking id to cancel")

    print("\n Success! test passed")
