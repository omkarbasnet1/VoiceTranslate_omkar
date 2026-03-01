"""
    Integration test for Sprint 3

    Tests the whole end to end
    voice file - whisper - AI agent - check response
"""
import os
import pytest
from datetime import datetime, timedelta
import whisper

from Room_booking_skills import (
    load_env,
    do_login,
    reserve_room,
    available_rooms,
    cancel_my_booking
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

    do_login(config["server_host"], config["user_email"], config["user_password"])
    agent = setup_agent()
    model = whisper.load_model("base")

    return agent, model


# integration test of voice AI
def test_end_agent(setup_data):
    agent, whisper_model = setup_data

    """
    print("\n Creating a test reservation...")
    target_time = (datetime.now() + timedelta(days=3)).replace(hour=14, minute=0, second=0)
    time_str = target_time.strftime("%Y-%m-%dT%H:%M:%S")

    rooms = available_rooms(host, token)
    assert rooms and len(rooms) > 0,"No rooms available to test."

    booking_result = None
    for room in rooms:
        room_id = room['id']
        print(f"Trying room {room_id}")
        booking_result = reserve_room(host, token, room_id, time_str, duration=15)

        if booking_result is not None:
            print(f"Booked room {room_id}")
            break
    assert  booking_result is not None, "failed to booking room"
    """

    print(" Reading voice file...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    audio_file = os.path.join(current_dir, "test_audio.wav")
    if not os.path.exists(audio_file):
        pytest.fail(f"Missing : {audio_file}")

    transcribed_text = audio_transcription(whisper_model, audio_file)
    assert len(transcribed_text) > 0
    print(f" Transcribed: {transcribed_text}")

    print(" Sending  to the AI agent...")
    ai_response = ask_agent(agent, transcribed_text)
    print(f" AI answer: {ai_response}")

    assert len(ai_response) > 0
    assert "Error" not in ai_response

    """
    print("\n Cleaning up reservation.")
    if booking_result:
        cancel_success = cancel_my_booking(host, token, booking_result)
        assert cancel_success is True, "Failed to remove the reservation"
    """

    print("\n Success! test passed")
