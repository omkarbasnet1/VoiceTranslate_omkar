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

    print("\n Success! test passed")
